<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import type { TrainingRecord, TrainingDetail } from '../types';
import { useMainStore } from '@/stores/main';

const route = useRoute();
const mainStore = useMainStore();

const fromTemplate = route.query.fromTemplate;//テンプレートからのクエリ
const templateId = route.query.templateId; //テンプレートからのクエリ。クエリで受け取ると文字列型となる
let tempIdCounter = 1; // 暫定記録ID用変数

// トレーニング記録用のテンプレート変数
//dateとdetails、detailsはさらにもう一階層ネストしたオブジェクト（=辞書型？）
const form = ref<TrainingRecord>({
  date: new Date().toISOString().split('T')[0],
  details: [
    {
      temp_id: tempIdCounter,//暫定ID追加
      exercise_id: 0,
      weight: 0,
      goal_reps: 0,
      goal_sets: 3,//見た目の観点からデフォルトで目標セット数を入れておくことにした
      sets: [],// 各セットのレップ数　数値型の配列(pythonでいうリスト形式？)を定義。[12,9,8]のように記す
      volume: 0,
    },
  ],
});



// 種目を追加する関数
const addExercise = () => {
  form.value.details.push({
    temp_id: tempIdCounter++,
    exercise_id: 0,
    weight: 0,
    goal_reps: 0,
    goal_sets: 3,
    sets: [] as number[],
    volume: 0,
  });
};

//ボリューム計算に関してビュー用(computed())とDBへのPOST時に共通する処理を関数化
//reduce()：配列の合計値を出すメソッド array.reduce((累積値, 現在の要素) => 累積値 + 現在の要素, 初期値)
//まどろこしい感じがあるが、配列の合計値を出すメソッドはreduce()しかない
function calculateVolume(detail: TrainingDetail): number {
  const repsTotal = detail.sets.reduce((sum, reps) => sum + reps, 0);
  return detail.weight * repsTotal;
};

// トータルレップ数を各種目ごとに計算してvolumes配列で返す関数
const volumes = computed(() =>
//map()は配列に対して操作し新たな配列を返すメソッド。
// const newArray = originalArray.map(任意の要素名 => {
//   処理して返す値が newArray に入る
  form.value.details.map(detail => calculateVolume(detail))
);

//テンプレート詳細データをTRN記録にセットする関数
//TemplateForm.vueのfillEdit()とほぼ同じだが一部に違いがあるのでストアで一元化は行わなかった
const setTemplate = () => {
  const template = mainStore.templates.find(t => t.id === Number(templateId));

  // templateがundefinedでないことを確認
  if (template) {
      while (form.value.details.length < template.details.length) {
          addExercise();
      }

      for (let i = 0; i < form.value.details.length; i++) {
          form.value.details[i].exercise_id = template.details[i].exercise_id;
          form.value.details[i].weight = template.details[i].weight;
          form.value.details[i].goal_reps = template.details[i].goal_reps;
          form.value.details[i].goal_sets = template.details[i].goal_sets;
      }

      alert(`テンプレート「${template.template_name}」をセットしました`);
  } else {
      // templateが見つからない場合の処理
      console.error(`テンプレートID「${templateId}」に一致するテンプレートが見つかりません`);
  }
};


//フォーム削除
const deleteForm = async (temp_id:number) => {
    form.value.details = form.value.details.filter(detail => detail.temp_id !== temp_id);
};



// TRN記録送信
const submitRecord = async () => {
  // DB送信前に volume を更新。forEachはmapと違い元の配列自体に変更を加えるため戻り値がない
  form.value.details.forEach(detail => {
    detail.volume = calculateVolume(detail);
  });

  const response = await fetch('http://127.0.0.1:5000/api/records', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value),
  });

  if (!response.ok) {
    alert('データ送信に失敗しました');
    return;
  }

  // フォームをリセット
  form.value = {
    date: new Date().toISOString().split('T')[0],
    details: [],
  };

  alert('トレーニング記録を保存しました');
};



// コンポーネントがマウント時に（URLアクセス時やページ更新時などにコンポーネントが
// 画面に表示される時）fetch()関数を実行してデータを取得する
onMounted(() => {
    mainStore.fetchExercise();
    if ( fromTemplate ){
      setTemplate();
    }
});

</script>


<template>
  <div 
    class="container d-flex flex-column justify-content-center align-items-center"
    style="min-height: 80vh;"
  >
    <!-- 入力フォーム -->
    <form v-on:submit.prevent="submitRecord">
      <div class="row my-3">
        <div class="form-group d-flex align-items-center mb-2"> 
          <label>日付
            <input 
              v-model="form.date" 
              required
              type="date" 
              style="height: 33px; border-radius: 5px;"
            />
          </label>
        </div> 
      </div> 
      
      <!-- gap:３列に並べた要素間の間隔を広げる -->
      <div 
        class="row"
        style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;"
      >
        <div 
          v-for="(detail, detailIndex) in form.details" 
          :key="detailIndex" 
          class="custom-card col mx-1"
        >
          <!-- 計画 -->
          <!-- 種目 -->
          <div class="form-group d-flex align-items-center mb-2">
            <label
              for="exercise"
              style="width: 120px; margin-right: 10px;">{{ detailIndex + 1 }}種目目
            </label>
            <select
              v-model="detail.exercise_id"
              required
              id="exercise"
              class="form-control"
              style=" width: 230px; height: 33px;"
            >
              <option 
                v-for="exercise in mainStore.exerciseOptions" 
                :value="exercise.id"
                :key="exercise.id"
              >
                {{ exercise.exercise_name }}
              </option>
            </select>
          </div>

          <div class="mt-2">計画：</div>

          <!-- 重量 -->
          <div class="form-group d-flex align-items-center mb-2">
            <label for="weight" class="label-field label-field-ml">重量 (kg)</label>
            <input
              v-model.number="detail.weight"
              required
              type="number"
              id="weight"
              class="form-control input-field"
            />
          </div>

          <!-- 目標レップ数 -->
          <div class="form-group d-flex align-items-center mb-2">
            <label for="goalReps" class="label-field label-field-ml">目標レップ数</label>
            <input
              v-model.number="detail.goal_reps"
              required
              type="number"
              id="goalReps"
              class="form-control input-field"
            />
          </div>

          <!-- 目標セット数 -->
          <div class="form-group d-flex align-items-center mb-2">
            <label for="goalSets" class="label-field label-field-ml">目標セット数</label>
            <input
              v-model.number="detail.goal_sets"
              required
              type="number"
              id="goalSets"
              class="form-control input-field" 
            />
          </div>

          
          <div class="mt-2">実施結果：</div>

          <!-- 実際のレップ数 -->
          <div 
            v-for="set in detail.goal_sets"
            :key="set"
            class="form-group d-flex align-items-center mb-2"
          >
            <label class="label-field label-field-ml">{{ set }}セット目:</label>
            <input
              v-model.number="detail.sets[set-1]"
              type="number"
              required
              class="form-control input-field"
            />
          </div>

          <!-- ボリューム表示 -->
          <div class="mt-2" style="text-align: center;">トータルボリューム: {{ volumes[detailIndex] }}</div>

          <button
            v-on:click="deleteForm(detail.temp_id)"
            class="btn-trash"
          >
            <i class="bi bi-trash"></i> <!-- ゴミ箱アイコン -->
          </button>
        </div>
      </div>

      <!-- 追加・保存ボタン -->
      <div class="d-flex justify-content-center mt-4"> <!-- フレックスボックスを使ってボタンを中央に配置 -->
        <button v-on:click="addExercise" class="custom-btn mx-1 mb-3" >種目を追加</button>
        <button type="submit" class="custom-btn mx-1 mb-3">記録を保存</button>
      </div>
    </form>
  </div>
</template>