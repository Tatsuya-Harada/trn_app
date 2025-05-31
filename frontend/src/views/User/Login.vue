<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink,useRouter } from 'vue-router';
import type { UserInformation } from '../../types';

const router = useRouter();

// ログイン情報入力用のテンプレート変数
const form = ref<UserInformation>({
    user_name:'',
    password: '',
})

// ログイン情報を送信する非同期関数
const submitRecord = async () => {
  const response = await fetch('http://127.0.0.1:5000/api/login', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value),
  });

  if (!response.ok) {
    alert('ログインに失敗しました');
    return;
  }

  // フォームをリセット
  form.value = {user_name:'',password:''};

  alert('ログインしました');

  // テンプレート詳細ページへ遷移
  router.push({name: 'Home'});

};

</script>

<template>
<!-- 入力フォームを作成しフォームのテンプレート変数にバインド -->
<div class="container d-flex flex-column justify-content-center align-items-center" style="min-height: 80vh;">
    <h1 class="mb-5">TRN管理App</h1>
    <!-- 入力フォーム -->
    <form v-on:submit.prevent="submitRecord">
      <div class="form-group d-flex align-items-center" style="margin-bottom: 10px;">
        <label style="width: 100px; margin-right: 10px; margin-left: 20px;">ユーザー名</label>
        <input v-model="form.user_name" required type="text" />
      </div>
      <div class="form-group d-flex align-items-center" style="margin-bottom: 10px;">
        <label style="width: 100px; margin-right: 10px; margin-left: 20px;">パスワード</label>
        <input v-model="form.password" required type="password" />
      </div>
      <div class="form-group d-flex justify-content-center align-items-center mt-5">
        <button class="custom-btn mb-3" type="submit">ログイン</button>
      </div>
    </form>

    <!-- ログイン・新規登録ボタン -->
    <div class="d-flex flex-column justify-content-center">
      <RouterLink class="button-link" v-bind:to="{name: 'Register'}">
        <button class="custom-btn">
          新規登録
        </button>
      </RouterLink>
    </div>
</div>

</template>

