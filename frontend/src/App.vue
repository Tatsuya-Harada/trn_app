<script setup lang="ts">
import {RouterView, RouterLink, useRoute, useRouter} from "vue-router";
import { useMainStore } from '@/stores/main';

const mainStore = useMainStore();
const route = useRoute(); // ログイン画面での表示制御に使用するため現在のルート情報を取得
const router = useRouter();
const hideLinksOnRoutes = ['Login', 'Register'];
const apiUrl = import.meta.env.VITE_API_URL; 

// ログアウト
const logout = async () => {
  const response = await fetch('${apiUrl}/logout', {
    method: 'POST',
    credentials: 'include', 
  });

  if (!response.ok) {
    alert('ログアウトできませんでした');
    return;
  }

  alert('ログアウトしました');

  // ログインページへ遷移
  router.push({name: 'Login'});
};

</script>

<template>
  <!-- 例：RobotoとNoto Sans JP を読み込む -->
<link 
	href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP&family=Roboto&display=swap" 
	rel="stylesheet"
>
<!-- 削除ボタンにゴミ箱アイコンを導入するために読み込み -->
<link
	rel="stylesheet"
	href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"
/>

<div class="d-flex min-vh-100 bg-dark-custom text-white">
	<!-- サイドバー -->
	<aside 
		v-if="!hideLinksOnRoutes.includes(String(route.name))" 
		class="position-fixed h-100 pt-3 px-3 bg-darker-custom text-white" 
		style="width: 230px; display: flex; flex-direction: column; justify-content: space-between;"
	>
	<div>
		<h2>TRN管理App</h2>
		<p>{{ mainStore.userInformation.user_name }}</p>
		<nav class="nav flex-column mt-3">
		<RouterLink v-bind:to="{ name: 'Home' }" class="router-link-button">ホーム</RouterLink>
		<RouterLink v-bind:to="{ name: 'TrainingRecord' }" class="router-link-button">記録</RouterLink>
		<RouterLink v-bind:to="{ name: 'ExerciseList' }" class="router-link-button">種目一覧</RouterLink>
		<RouterLink v-bind:to="{ name: 'TemplateList' }" class="router-link-button">テンプレート一覧</RouterLink>
		</nav>
	</div>
	
	<!-- ログアウトボタンをサイドバー下部に配置 -->
	<button v-on:click="logout" class="btn btn-outline-danger mt-3 mb-5">ログアウト</button>
	</aside>

	<!-- メインコンテンツ -->
	<main
		class="flex-grow-1 mt-3"
		v-bind:style="{marginLeft: hideLinksOnRoutes.includes(String(route.name)) ? '0':'230px'}"
		style="overflow: auto"
	>
	<RouterView />
	</main>
</div>

</template>