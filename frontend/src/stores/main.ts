import { ref } from 'vue';
import {defineStore} from "pinia";
import type { Exercise, Template, TemplateDetail, UserInformation } from '../types';

//GPTによると今までエラーが出ていた書き方はオプション型と呼ばれるもので型推論が行われずにエラーが出やすいので
//以下のような型を明示するSetup型を提案され試したとことエラーがなくなった。vue3との相性はこちらの方がよりいいとのこと
export const useMainStore = defineStore('main', () => {
  //state:refを使いstateを定義
  const exerciseOptions = ref<Exercise[]>([]);
  const form_exercise = ref<Exercise>({ exercise_name: '', memo: '',});
  const selectedTemplate = ref({ template_id:0, template_name: '',});
  const templateDetails = ref<TemplateDetail[]>([]); 
  const templates = ref<Template[]>([]); 
  const userInformation = ref<UserInformation>({user_id:0,user_name:'',});

  const apiUrl = import.meta.env.VITE_API_URL; 
  //actionsに当たる部分
  //stateに加工処理をしたgettersを設定したい場合はオプション型同様computedプロパティで定義する
  // 種目一覧取得
  const fetchExercise = async () => {
    const response = await fetch(`${apiUrl}/exercise`,{
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error(`HTTPエラー: ${response.status}`);
    }
    exerciseOptions.value = await response.json();
  };

  // 新規種目追加
  const submitExercise = async () => {
    const response = await fetch(`${apiUrl}/exercise`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form_exercise.value),
    });

    if (!response.ok) {
      alert('データ送信に失敗しました');
      return;
    }

    form_exercise.value = {
      exercise_name: '',
      memo: '',
    };

    alert('種目を新規追加しました');
    await fetchExercise();
  };

  // ログインしているかの確認、ログインユーザー情報の取得
  const fetchLoginUser = async () => {
    const response = await fetch(`${apiUrl}/me`,{
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`HTTPエラー: ${response.status}`);
    }
    
    userInformation.value = await response.json();
  };

  return {
    exerciseOptions,
    form_exercise,
    fetchExercise,
    submitExercise,
    selectedTemplate,
    templateDetails,
    templates,
    fetchLoginUser,
    userInformation,
  };
});