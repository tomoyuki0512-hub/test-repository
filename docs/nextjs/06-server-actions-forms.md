---
title: ⑥ Server Actionsとフォーム
---

# ⑥ Server Actionsとフォーム — APIを作らずに更新処理を書く

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑤ データ取得とキャッシュ](05-data-fetching-caching.md) ｜ 次 → [⑦ スタイリングとUI](07-styling-ui.md)

[⑤](05-data-fetching-caching.md) では「読む」を扱いました。この章は「**書く**」です。Server Actions によって、フォーム送信のためにAPIエンドポイントを作る必要がなくなります。

---

## 1. Server Actions とは

**サーバー上で動く関数を、クライアントから直接呼べる仕組み**です。

```
従来（REST API）                     Server Actions
─────────────────────                ─────────────────────
1. app/api/posts/route.ts を書く      1. 関数を書く
2. リクエストの型を決める              2. 呼ぶ
3. fetch('/api/posts', {...}) を書く   以上
4. レスポンスの型を合わせる
5. エラーハンドリングを書く
```

裏側ではNext.jsが自動でHTTPリクエストを組み立てているのですが、**書く側からは「関数を呼んでいる」ようにしか見えません**。

---

## 2. 最小の例

```ts
// app/posts/actions.ts
'use server'                      // ← ファイル先頭。これがServer Actionの宣言

import { db } from '@/lib/db'
import { revalidateTag } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  await db.post.create({ data: { title } })
  revalidateTag('posts')          // 一覧のキャッシュを破棄
}
```

```tsx
// app/posts/page.tsx （Server Component のままでよい）
import { createPost } from './actions'

export default function Page() {
  return (
    <form action={createPost}>     {/* action に関数を直接渡す */}
      <input name="title" required />
      <button type="submit">作成</button>
    </form>
  )
}
```

**`'use client'` が1つも要らない**点に注目してください。JavaScriptが無効な環境でも、これはHTMLの標準フォームとして動作します（プログレッシブエンハンスメント）。

### `'use server'` の2つの書き方

```ts
// ① ファイル全体をServer Actionにする（推奨。テストもしやすい）
'use server'
export async function createPost() { ... }
```

```tsx
// ② インラインで定義する（Server Component内でのみ）
export default function Page() {
  async function createPost(formData: FormData) {
    'use server'
    ...
  }
  return <form action={createPost}>...</form>
}
```

> ⚠️ `'use server'` と `'use client'` は**まったく逆の意味**です。`'use client'` は「クライアントに送る」、`'use server'` は「サーバー専用の関数として公開する」。名前が似ているので混同しないでください。

---

## 3. 実務レベルのフォーム：`useActionState`

実際にはバリデーションエラーの表示や送信中の状態が必要です。React 19 の `useActionState` を使います。

### アクション側

```ts
// app/posts/actions.ts
'use server'

import { z } from 'zod'
import { revalidateTag } from 'next/cache'
import { redirect } from 'next/navigation'

const PostSchema = z.object({
  title: z.string().min(1, 'タイトルは必須です').max(100, '100文字以内です'),
  body: z.string().min(10, '本文は10文字以上必要です'),
})

export type State = {
  errors?: { title?: string[]; body?: string[] }
  message?: string
}

export async function createPost(prevState: State, formData: FormData): Promise<State> {
  // 1. 認証（必須）
  const user = await getCurrentUser()
  if (!user) return { message: 'ログインが必要です' }

  // 2. バリデーション（必須）
  const parsed = PostSchema.safeParse({
    title: formData.get('title'),
    body: formData.get('body'),
  })
  if (!parsed.success) {
    return { errors: z.flattenError(parsed.error).fieldErrors }
  }

  // 3. 実行
  try {
    await db.post.create({ data: { ...parsed.data, authorId: user.id } })
  } catch {
    return { message: '保存に失敗しました' }
  }

  // 4. キャッシュ破棄 → 遷移
  revalidateTag('posts')
  redirect('/posts')
}
```

### フォーム側

```tsx
'use client'

import { useActionState } from 'react'
import { useFormStatus } from 'react-dom'
import { createPost, type State } from './actions'

const initialState: State = {}

export function PostForm() {
  const [state, formAction] = useActionState(createPost, initialState)

  return (
    <form action={formAction}>
      <input name="title" />
      {state.errors?.title?.map((e) => <p key={e} className="text-red-600">{e}</p>)}

      <textarea name="body" />
      {state.errors?.body?.map((e) => <p key={e} className="text-red-600">{e}</p>)}

      {state.message && <p className="text-red-600">{state.message}</p>}
      <SubmitButton />
    </form>
  )
}

// 送信中の状態は子コンポーネントで取る
function SubmitButton() {
  const { pending } = useFormStatus()
  return (
    <button type="submit" disabled={pending}>
      {pending ? '送信中...' : '作成'}
    </button>
  )
}
```

> 💡 **`useFormStatus` は「`<form>` の子孫でしか動かない」**ため、送信ボタンを別コンポーネントに切り出す必要があります。同じコンポーネント内で呼んでも `pending` は常に `false` です。これは非常によくあるハマりどころです。

---

## 4. 引数付きで呼ぶ（`bind`）

「この記事を削除」のようにIDを渡したい場合、`bind` を使います。

```tsx
import { deletePost } from './actions'

export function DeleteButton({ id }: { id: string }) {
  const deletePostWithId = deletePost.bind(null, id)
  return (
    <form action={deletePostWithId}>
      <button type="submit">削除</button>
    </form>
  )
}
```

> ⚠️ **`<input type="hidden" name="id">` でIDを渡すのは危険**です。ブラウザの開発者ツールで値を書き換えれば他人の投稿を削除できてしまいます。`bind` を使うか、**サーバー側で必ず所有者チェック**をしてください（後述）。

---

## 5. 楽観的更新（`useOptimistic`）

サーバーの応答を待たず、**先に画面を更新して体感速度を上げる**手法です。「いいね」ボタンなどに使います。

```tsx
'use client'
import { useOptimistic } from 'react'
import { toggleLike } from './actions'

export function LikeButton({ postId, likes }: { postId: string; likes: number }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (current: number, delta: number) => current + delta
  )

  return (
    <form action={async () => {
      addOptimisticLike(1)        // 即座に画面へ反映
      await toggleLike(postId)    // 裏でサーバー処理
    }}>
      <button type="submit">❤️ {optimisticLikes}</button>
    </form>
  )
}
```

サーバー処理が失敗した場合、Reactが自動的に元の値へ巻き戻します。

---

## 6. 🚨 セキュリティ — この章で最も重要

**Server Action は、実質的に「公開されたAPIエンドポイント」です。** Next.jsが自動生成するIDを知っていれば、フォームを経由せず誰でも直接POSTできます。

### 必ず守る3原則

```ts
'use server'

export async function deletePost(postId: string) {
  // ① 認証：誰であるかを確認する
  const user = await getCurrentUser()
  if (!user) throw new Error('Unauthorized')

  // ② 認可：その人にその操作の権限があるか確認する
  const post = await db.post.findUnique({ where: { id: postId } })
  if (!post) throw new Error('Not found')
  if (post.authorId !== user.id && user.role !== 'admin') {
    throw new Error('Forbidden')
  }

  // ③ バリデーション：引数は一切信用しない
  //    （ここでは postId の存在確認が兼ねている）

  await db.post.delete({ where: { id: postId } })
  revalidateTag('posts')
}
```

### やりがちな危険パターン

| ❌ 危険 | なぜ危険か | ✅ 正しく |
| --- | --- | --- |
| クライアントで認証チェックだけして、Actionではしない | Actionを直接叩けば素通り | **Action内で必ずチェック** |
| `hidden` フィールドでユーザーIDを渡す | 書き換えられる | サーバーでセッションから取得 |
| `where: { id }` だけでdelete | 他人のデータも消せる | `where: { id, authorId: user.id }` |
| `proxy.ts` の認証だけに頼る | Actionは経路が異なる場合がある | データアクセス層でも確認 |
| エラーをそのまま `throw` | DB構造などが漏れる可能性 | メッセージを整形して返す |

> 🔑 **覚え方**：`'use server'` と書いた関数は、**インターネットに公開したURLと同じ**だと思ってください。「画面から呼ばれるはず」という前提は成立しません。

### 併せて確認すること

- **レート制限**：連打・総当たりを防ぐ（Upstash Ratelimit などを利用）
- **`allowedOrigins`**：リバースプロキシ配下では `next.config.ts` の `experimental.serverActions.allowedOrigins` の設定が必要な場合があります
- **サイズ上限**：ファイルアップロードでは `bodySizeLimit` を確認

---

## 7. Server Actions を使うべきでない場面

万能ではありません。次の場合は **Route Handler（`route.ts`）** を使ってください（→ [⑨](09-route-handlers-api.md)）。

| 場面 | 理由 |
| --- | --- |
| 外部サービスからのWebhook受信 | 決まったURLとHTTPメソッドが必要 |
| モバイルアプリ・他システムから呼ぶAPI | Server ActionsはNext.js内部の仕組み |
| GETでデータを返すだけの処理 | Server Actionsは常にPOST。キャッシュも効かない |
| ファイルのストリーミング配信 | Responseを細かく制御したい |
| OAuthのコールバック | 特定のURL形式が要求される |

---

## 8. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| `Functions cannot be passed directly...` | `'use server'` を書き忘れ | ファイル先頭に追加 |
| `pending` が常に `false` | `useFormStatus` を `<form>` と同じ階層で呼んでいる | 子コンポーネントに切り出す |
| 送信後も一覧が古い | キャッシュを破棄していない | `revalidateTag` / `updateTag`（→ [⑤](05-data-fetching-caching.md)） |
| `redirect()` でエラーが出る | `try/catch` の中で呼んでいる | `redirect` は例外で実装されている。**`try` の外**で呼ぶ |
| 入力値が消える | エラー時に値を返していない | stateに入力値も含めて返す |

---

## 9. この章のまとめ

- **Server Actions＝APIを書かずに更新処理が書ける仕組み**。`'use server'` で宣言
- 単純なフォームは `<form action={fn}>` だけで動く（JS不要）
- 実務では **`useActionState` ＋ Zod** が定石。送信中は `useFormStatus`（子で呼ぶ）
- IDは `bind` で渡す。**`hidden` フィールドは書き換えられる**
- 🚨 **Server Action は公開APIと同じ。認証・認可・バリデーションを必ずAction内で行う**
- Webhook・外部公開API・GET処理は Route Handler の担当

---

次の章 → [⑦ スタイリングとUI](07-styling-ui.md)
