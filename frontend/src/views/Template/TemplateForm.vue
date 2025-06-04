<script setup lang="ts">
import { ref,onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Template } from '../../types';
import { useMainStore } from '@/stores/main';

const router = useRouter();
const route = useRoute();
const mainStore = useMainStore();

const isEditing = route.query.isEditing;//テンプレートからのクエリ
const templateId = route.query.templateId;
const apiUrl = import.meta.env.VITE_API_URL; 

// TRNテンプレート新規追加用のテンプレート変数
let tempIdCounter = 1;
const form = ref<Template>({
  template_name: '',
  details: [
    {
      temp_id: tempIdCounter,//暫定ID追加
      id:0,
      exercise_id: 0,
      weight: 0,
      goal_reps: 0,
      goal_sets: 0,
    },
  ],
});



//更新用にテンプレート詳細データを編集フォームに転記する関数
const fillEditForm = () => {
  // フォームをリセット
  form.value = { template_name: '', details: [] };

  const template = mainStore.templates.find(t => t.id === Number(templateId));

  // templateがundefinedでないことを確認
  if (template) {
    form.value.template_name = template.template_name;

    while (form.value.details.length < template.details.length) {
      addExercise();
    }

    for (let i = 0; i < form.value.details.length; i++) {
      form.value.details[i].id = template.details[i].id;
      form.value.details[i].exercise_id = template.details[i].exercise_id;
      form.value.details[i].weight = template.details[i].weight;
      form.value.details[i].goal_reps = template.details[i].goal_reps;
      form.value.details[i].goal_sets = template.details[i].goal_sets;
    }
  } else {
    // templateが見つからなかった場合の処理
    console.error(`Template with id ${templateId} not found.`);
  }
};


// 種目を追加する関数
const addExercise = () => {
  form.value.details.push({
    temp_id: tempIdCounter++,
    exercise_id: 0,
    weight: 0,
    goal_reps: 0,
    goal_sets: 0,
  });
};



// TRNテンプレート保存
const submitRecord = async () => {

  const response = await fetch(`${apiUrl}/template`, {
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
    template_name: '',
    details: [],
  };

  alert('テンプレートを保存しました');

  // テンプレート一覧ページへ遷移
  router.push(
    {name: 'TemplateList'}
  );

};

//更新したTRNテンプレートを送信
const changeRecord = async (template_id:number) => {

  const url = new URL('${apiUrl}/template');
  if (template_id) {
    url.searchParams.append('template_id', String(template_id)); //idは文字列として扱われるためBEで数値に戻す
  }
  const response = await fetch(url.toString(), {
    method: 'PUT',
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
    template_name: '',
    details: [],
  };

  alert('テンプレートを更新しました');

  // テンプレート一覧ページへ遷移
  router.push({name: 'TemplateList'});

};

//新規追加時・編集時に種目とそれに関連するレコードを削除する関数
//新規追加時の場合、詳細ID確定前のため他の識別子（一時IDを付与するのが一般的）を用いて該当のオブジェクトをformから削除
//isEditingで判断し更新時の場合は、DBから取得したデータの場合(テンプレート詳細IDあり？)はDBも削除
// すでに設定を保存しているものとそうでないものでアラートが出るかどうかに差が出るので今回はアラートを削除
const deleteDetail = async (temp_id:number,id:number) => {
  //更新の場合でDBにデータが存在する場合はDB上のデータも削除
  if (isEditing && id) {
    const url = new URL('${apiUrl}/template/detail');
    url.searchParams.append('detail_id', String(id));

    await fetch(url.toString(), {
      method: 'DELETE',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    });
  }
  //新規追加・更新データにかかわらずフォームから削除
  //form.detailsにtemp_idを持つオブジェクト以外のオブジェクトを再代入している
  //詳細レコードを再取得する
  form.value.details = form.value.details.filter(detail => detail.temp_id !== temp_id);
};

//isEditingのステータスで新規追加か更新の関数を実行する関数を定義
const submitOrChangeRecord = () =>{
  if ( isEditing ){
    changeRecord( Number(templateId) )
  }
  else {
    submitRecord()
  }
};

onMounted(() => {
  mainStore.fetchExercise();
  if ( isEditing ){
    fillEditForm();
  }
});

</script>

<template>
  <div
    class="container d-flex flex-column justify-content-center align-items-center"
    style="min-height: 80vh;"
  >
      <!-- 入力フォーム -->
      <!-- isEditing変数で更新か新規追加かを判断し表示を変える -->
      <!-- @click="addExercise"で追加した種目だけdetailsにはオブジェクトが格納されているのでforループで取り出す -->
      <form v-on:submit.prevent="submitOrChangeRecord">
          <div class="row my-3">
            <label>
              テンプレート名
              <input
                v-model="form.template_name"
                required type="string"
                style="width: 300px; height: 33px; border-radius: 5px;"
              />
            </label>
          </div>

          <div
            class="row" 
            style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;"
          >
            <div
              v-for="(detail, detailIndex) in form.details"
              :key="detailIndex"
              class="custom-card mx-2"
            >
              
              <!-- 種目 -->
              <div class="form-group d-flex align-items-center" style="margin-bottom: 10px;">
                <label style="width: 100px; margin-right: 10px;">{{ detailIndex + 1 }}種目</label>
                <!-- 種目をDBから取得しセレクトボックス形式に変更-->
                <!-- 表示する選択肢は種目名だが、送信する値はそのidなので:value="exercise.id" -->
                <select
                  v-model="detail.exercise_id"
                  required
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
              
              <!-- 重量 -->
              <div class="form-group d-flex align-items-center mb-2">
                <label for="weight" class="label-field">重量 (kg) </label>
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
                <label for="goalReps" class="label-field">目標レップ数</label>
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
                <label for="goalSets" class="label-field">目標セット数</label>
                <input
                  v-model.number="detail.goal_sets"
                  required
                  type="number"
                  id="goalSets"
                  class="form-control input-field"
                />
              </div>

              <button v-on:click="deleteDetail(detail.temp_id,Number(detail.id))" class="btn-trash">
                <i class="bi bi-trash"></i> <!-- ゴミ箱アイコン -->
              </button>
            </div>
          </div>
          
          <div class="d-flex justify-content-center mt-4">
            <!-- 種目追加ボタン -->
            <button
              type="button"
              v-on:click="addExercise()"
              class="custom-btn mx-1 mb-3"
            >
              種目を追加
            </button>

            <!-- テンプレートを更新or保存ボタン -->
            <!-- isEditing変数で更新か新規追加かを判断し表示を変える -->
            <button
              type="submit" 
              class="custom-btn mx-1 mb-3"
            >
              {{ isEditing ? 'テンプレートを更新' : 'テンプレートを保存' }}
            </button>

          </div>
    </form>
  </div>

</template>