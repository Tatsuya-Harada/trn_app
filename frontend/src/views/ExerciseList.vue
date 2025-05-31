<script setup lang="ts">
import { ref,onMounted } from 'vue';
import { useMainStore } from '@/stores/main';

const mainStore = useMainStore();
const showModal = ref(false); // モーダルの表示状態を管理する変数

//種目削除
const deleteRecord = async (exercise_id:number) => {

    const url = new URL('http://127.0.0.1:5000/api/exercise');
    if (exercise_id) {
      url.searchParams.append('exercise_id', String(exercise_id));
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

    alert('種目を削除しました');

    mainStore.fetchExercise();
};

//種目を新規追加時に種目一覧も更新されるように２つの関数をまとめた関数を定義しv-onにバインドする
const handleSubmit = async () => {
  await mainStore.submitExercise();
  await mainStore.fetchExercise();
  showModal.value = false;  // モーダルを閉じる
};



//コンポーネントがマウント時に（URLアクセス時やページ更新時などにコンポーネントが
//画面に表示される時）fetch()関数を実行してデータを取得する
onMounted(() => {
  mainStore.fetchExercise();
});

</script>

<template>
  <div 
    class="container d-flex flex-column justify-content-center align-items-center" 
    style="min-height: 80vh;"
  >
    <!-- 新規追加ボタン -->
    <div class="row my-3">
      <button class="custom-btn" @click="showModal = true">種目を新規追加</button>
    </div>

    <!-- モーダル -->
    <b-modal v-model="showModal" title="新規種目追加" hide-footer>
      <form v-on:submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="exerciseName">種目名</label>
          <input
            v-model="mainStore.form_exercise.exercise_name"
            required
            type="text"
            id="exerciseName"
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="memo">メモ</label>
          <input
            v-model="mainStore.form_exercise.memo"
            type="text"
            id="memo"
            class="form-control"
          />
        </div>

        <div class="d-flex justify-content-center mt-4"> <!-- mt-4でフォームからボタンを少し離す -->
          <!-- 追加ボタン（アウトラインスタイル） -->
          <b-button
            type="submit"
            variant="outline-success"
            class="mx-2"
          >追加
          </b-button> <!-- 成功色のアウトライン -->
          
          <!-- キャンセルボタン（アウトラインスタイル） -->
          <b-button
            v-on:click="showModal = false"
            variant="outline-danger"
            class="mx-2"
          >キャンセル
          </b-button> <!-- 警告色のアウトライン -->
        </div>
      </form>
    </b-modal>

    <!-- 種目テーブル -->
    <div class="row" style="width: 90%;">
      <table class="custom-table" style="table-layout: fixed; width: 100%;">
      <thead>
          <tr>
          <!-- 列名はハードコーディングでOK -->
          <th style="width: 40%;">種目名</th>
          <th style="width: 55%;">メモ</th>
          <th style="width: 5%;"></th>
          </tr>
      </thead>
      <tbody>
          <!-- v-forは基本的に繰り返したい要素タグに記述する -->
          <tr v-for="exercise in mainStore.exerciseOptions" :key="exercise.id">
          <td>{{ exercise.exercise_name }}</td>
          <td>{{ exercise.memo }}</td>
          <td v-if="exercise.id !== undefined"> <!-- exercise.idがundefinedの型えらにならないようにv-ifでチェック -->
            <button v-on:click.prevent="deleteRecord(exercise.id)" class="btn-trash">
              <i class="bi bi-trash"></i> <!-- ゴミ箱アイコン -->
            </button>
          </td>
          </tr>
      </tbody>
      </table>
    </div>

  </div>
</template>