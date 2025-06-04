<script setup lang="ts">
import { onMounted } from 'vue';
import { RouterLink } from "vue-router";
import { useMainStore } from '@/stores/main';

const mainStore = useMainStore();
const apiUrl = import.meta.env.VITE_API_URL; 



// テンプレート一覧取得
const fetchTemplate = async () => {    
  const response = await fetch('${apiUrl}/template',{
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error(`HTTPエラー: ${response.status}`);
  }

  mainStore.templates = await response.json();
};

//TRNテンプレート削除
const deleteRecord = async (template_id:number) => {

  const url = new URL('${apiUrl}/template');

  if (template_id) {
    url.searchParams.append('template_id', String(template_id));
  }

  const response = await fetch(url.toString(), {
    method: 'DELETE',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    alert('データ送信に失敗しました');
    return;
  }

  alert('テンプレートを削除しました');

  fetchTemplate();
};



onMounted(() => {
  fetchTemplate();
});

</script>

<template>
  <div
    class="container d-flex flex-column justify-content-center align-items-center"
    style="min-height: 80vh;"
  >
    <!-- 新規追加ボタン -->
    <div class="row my-3">
      <RouterLink v-bind:to="{ name: 'TemplateForm' }">
      <button class="custom-btn">
        テンプレートを新規追加
      </button>
      </RouterLink>
    </div>   
        
  <!-- テンプレート -->
    <div
      class="row"
      style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; width: 90%;"
    >
    <div v-for="template in mainStore.templates" :key="template.id">
      <div class="col" >

        <!-- テンプレート名・詳細 -->
        <h4>{{template.template_name}}</h4>
        <table class="custom-table">
          <thead>
            <tr>
              <th>種目名</th>
              <th>重量(kg)</th>
              <th>レップ数</th>
              <th>セット数</th>
            </tr>
          </thead>
          <tbody>
            <!-- v-forは基本的に繰り返したい要素タグに記述する -->
            <tr  v-for ="detail in template.details ">
              <td>{{ detail.exercise_name }}</td>
              <td>{{ detail.weight }}</td>
              <td>{{ detail.goal_reps }}</td>
              <td>{{ detail.goal_sets }}</td>
            </tr>
          </tbody>
        </table>

        <!-- セット・編集・削除ボタン -->
        <div class="d-flex justify-content-center mt-3 mb-5">
          <RouterLink
            class="button-link"
            v-bind:to="{
              name: 'TrainingRecord',
              query: {
                fromTemplate: 'true',
                templateId: template.id
            }}"
          >
            <button class="custom-btn mx-1">TRN記録にセット</button>
          </RouterLink>

          <RouterLink
            class="button-link"
            v-bind:to="{
              name: 'TemplateForm',
              query: {
                isEditing: 'true',
                templateId: template.id
            }}"
          >
            <button class="custom-btn mx-1" style="width: 100px;">編集</button>
          </RouterLink>

          <button
            v-on:click.prevent="deleteRecord(Number(template.id))"
            class="btn-trash-dark"
          >
            <i class="bi bi-trash"></i> <!-- ゴミ箱アイコン -->
          </button>
        </div>
        </div>
      </div>
    </div> 
  </div>

</template>

<style scoped>
.custom-table {
  width: 100%;
  /* border-collapse: separate; */
  border-spacing: 0 10px; /* 列間隔と行間隔の調整 */
}

.custom-table th, .custom-table td {
  /* padding: 10px 15px; thとtdの内側の余白を調整 */
  /* border: 1px solid #ddd; セルの枠線 */
}

.custom-table th {
  background-color: #f8f9fa; /*ヘッダー行の背景色 */
  text-align: left; /* ヘッダーは左寄せ */
}

.custom-table td {
  text-align: left; /* デフォルトでは左寄せ */
}

/* 数値を右寄せにする */
.custom-table td:nth-child(3), .custom-table td:nth-child(4), .custom-table td:nth-child(5) {
  text-align: center;
}

</style>