<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { GraphSetting } from '../types';
import { Line } from 'vue-chartjs'//線グラフを表示するコンポーネント
import {Chart as ChartJS,Title,Tooltip,Legend,LineElement,CategoryScale,LinearScale,PointElement} from 'chart.js'
import { useMainStore } from '@/stores/main';
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const mainStore = useMainStore();
const chartData = ref<any[]>([]); //グラフデータ
//const settings = ref<GraphSetting[]>([]) //グラフ設定データ
const apiUrl = import.meta.env.VITE_API_URL; 

// 空のグラフデータ
const emptyChartData = {
  labels: [], // ラベルは空
  datasets: [
    {
      label: '重量の推移 (kg)',
      data: [], // データは空
      borderColor: 'rgba(40, 100, 255, 1)',
      backgroundColor: 'rgba(40, 100, 255, 0.2)',
      tension: 0.3,
    },
    {
      label: 'ボリューム',
      data: [], // ボリュームも空
      borderColor: 'rgba(0, 175, 100, 1))',
      backgroundColor: 'rgba(0, 175, 100, 0.2)',
      tension: 0.3,
    }
  ]
}

//グラフ表示用の進捗データ
//datasets配列にオブジェクトを複数入れることで１つのグラフに複数のデータを表示可能
let tempIdCounter = 1;

// chartOptions は グラフの見た目や挙動をカスタマイズするための設定オブジェクト。表示するデータと別に用意するのが基本
const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' as const },
  },
  scales: {
    weightAxis: {
      type: 'linear' as const,
      position: 'left' as const,
      title: {
        display: true,
        text: '重量 (kg)',
      },
    },
    volumeAxis: {
      type: 'linear' as const,
      position: 'right' as const,
      title: {
        display: true,
        text: 'ボリューム',
      },
      grid: {
        drawOnChartArea: false, // 右側のグリッド非表示（重なりを避ける）
      },
    },
  },
};

//v-forをfetchのたびに強制再実行させるのに使用するテンプレート変数。forceRerenderでカウントアップ
const renderKey = ref(0);

//fetch()でデータ取得後にグラフ描画が始まるようにステータス管理
const isDataReady = ref(false);



//chartDataのdatasetsを作成する関数。共有参照されないようにディープコピーして使う
const createNewDatasets = () => [
    {
      label: '重量の推移 (kg)',
      data: [] as number[],  // 重量データ ex:[10, 20, 30]
      borderColor: 'rgba(40, 100, 255, 1)',
      backgroundColor: 'rgba(40, 100, 255, 0.2)',
      tension: 0.3,
      yAxisID: 'weightAxis', // chartOptions>scalesのキー名に合わせる
    },
    {
      label: 'ボリューム',
      data: [] as number[], // ボリュームデータ
      borderColor: 'rgba(0, 175, 100, 1)',
      backgroundColor: 'rgba(0, 175, 100, 0.2)',
      tension: 0.3,
      yAxisID: 'volumeAxis', // 右軸を指定
    },
  ]

//グラフデータを追加する関数
const addChartDatum = () => {
  chartData.value.push({
    id:null,
    temp_id: tempIdCounter++,
    exercise_id: null,
    labels: [] as string[],
    isDataReady: false,
    datasets: createNewDatasets()
  },)
};

//データが変わったときに再描画を促すためにrenderKeyをカウントアップ
const forceRerender = () => {
  renderKey.value++; // 値を変えることで再描画
};



//記録取得(グラフ表示用)
const fetchData = async (chart_datum_id:number,exercise_id?: number) => {
  isDataReady.value = false;

  // const url = new URL('http://127.0.0.1:5000/api/records');
  const url = new URL(`${apiUrl}/records`);

  if (exercise_id) {
    url.searchParams.append('exercise_id', String(exercise_id)); //exercise_idは文字列として扱われるためBEで数値に戻す
  }

  const response = await fetch(url.toString(),{
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error(`HTTPエラー: ${response.status}`);
  }

  const data = await response.json();

  // 日付を時系列順にソート
  //アロー関数を使いsort()に２つの日付データを比較する関数そのものが引数として渡される
  //Date(a.date).getTime()で日付がmm秒で返されるのでその差が正か負かで大小を判定
  const sorted = data.sort((a: any, b: any) => {
    return new Date(a.date).getTime() - new Date(b.date).getTime();
  });

  // ラベル（日付文字列）とデータ（重量）を取り出す
  const labels: string[] = [];
  const weights: number[] = [];
  const volumes: number[]=[];

  for (const item of sorted) {
    const dateStr = item.date; // e.g., '2025-04-10'
    const details = item.details;

    for (const detail of details) {
      labels.push(dateStr);
      weights.push(detail.weight);
      volumes.push(detail.volume);
    }
  }

  //グラフ表示用オブジェクトに取得したデータを格納
  const index = chartData.value.findIndex(item => item.temp_id === chart_datum_id);//該当のtemp_idを持つchardataのインデックスを取得
  chartData.value[index].labels = labels;
  chartData.value[index].datasets[0].data = weights;
  chartData.value[index].datasets[1].data = volumes;
  chartData.value[index].isDataReady = true;

  console.log('chartData:', chartData.value);
  forceRerender();
};

//グラフ設定を送信
const saveSettings = async () => {
  // temp_idごとの種目IDを配列形式に整形（順序も記録）
  const payload = chartData.value.map((datum, index) => ({
    exercise_id: datum.exercise_id,
    order: index
  }));
  //出力例
  //   payload = [
  //   { exercise_id: 1, order: 0 },
  //   { exercise_id: 5, order: 1 },
  //   { exercise_id: 3, order: 2 },
  // ];

  const response = await fetch('http://127.0.0.1:5000/api/graph-settings', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

  if (!response.ok) {
    alert('データ送信に失敗しました');
    return;
  }

  alert('設定を保存しました');

  //「グラフ設定を保存」を押した直後に描画されている保存したグラフの設定はまだDBから
  // 参照してきているわけではないので仮に保存後すぐに削除してもDB上からは消えずホームに戻ってくるとDBから設定を取得して再度表示されてしまう
  //解消のため以下のリロードを入れたが、画面の切り替わりが一瞬起きるため見た目的にあまり良くなくベストとは言えない
  location.reload();

};

// グラフ設定の取得
const fetchGraphSettings = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/graph-settings', {
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`HTTPエラー: ${response.status}`);
    }
    //表示順に並んだ種目idデータを取得
    //変数をページ上部で定義してからsettingsをここで使う形だとうまくいかないため、ここで直接型を定義するgptの方法を採用
    const settings:GraphSetting[] = await response.json();

    settings.forEach((setting) => {
      const temp_id = tempIdCounter++;

      chartData.value.push({
        id:setting.id,
        temp_id: temp_id,
        exercise_id:setting.exercise_id,
        labels: [],
        isDataReady: false,
        datasets: createNewDatasets()
      });

      // 各グラフのデータを取得
      fetchData(temp_id, setting.exercise_id);
    });
};

//グラフ設定の削除
// TemplateForm.vueを参考に、DBに記録されてる設定（idがあるかで判断？）はバックエンドに削除リクエストし、
// 新規追加・更新データにかかわらずchartDataから該当のグラフデータを削除
 // すでに設定を保存しているものとそうでないものでアラートが出るかどうかに差が出るので今回はアラートを削除
const deleteGraphSettings = async (chart_temp_id:number, setting_id:number) => {
    //更新の場合でDBにデータが存在する場合はDB上のデータも削除
    if ( setting_id) {
        const url = new URL('http://127.0.0.1:5000/api/graph-settings');
        url.searchParams.append('setting_id', String(setting_id));

        await fetch(url.toString(), {
          method: 'DELETE',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
        });
    }

    //新規追加・更新データにかかわらずフォームから削除
    //temp_idを持つオブジェクト以外のオブジェクトをchartData.valueに再代入＝temp_id持つレコードだけ削除
    //アロー関数 datum => datum.temp_id !== chart_temp_id で temp_idを持たない要素はtrueで返されfilterメソッドでtrueの要素だけ中種される
    chartData.value = chartData.value.filter(datum => datum.temp_id !== chart_temp_id);

};



// コンポーネントがマウント時に（URLアクセス時やページ更新時などにコンポーネントが
// 画面に表示される時）fetchData()関数を実行してデータを取得する
onMounted(async() => {
  await mainStore.fetchLoginUser();
  await mainStore.fetchExercise();
  await fetchGraphSettings()
});

</script>

<template>
  <div 
    class="container d-flex flex-column justify-content-center align-items-center"
    style="min-height: 100vh; gap: 50px;"
    :key="renderKey"
  >
    <div 
    class="row" 
    style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; width: 100%;"
    >
      <div v-for="chartDatum in chartData" :key="chartDatum.temp_id" class="col">

        <!-- グラフ -->
        <Line 
          v-if="chartDatum.isDataReady" 
          :data="chartDatum" 
          :options="chartOptions" 
          :key="chartDatum.temp_id + '-' + chartDatum.exercise_id" 
        />
        <Line 
          v-else
          :data="emptyChartData"
          :options="chartOptions" 
          :key="'empty-' + chartDatum.temp_id" 
        /><!-- データが準備できていない場合でも、空のデータでグラフを表示 -->

        <!-- 種目セレクトボックス・削除ボタン -->
        <div class="d-flex justify-content-center mt-1">
          <div class="form-group">
            <select 
              v-model="chartDatum.exercise_id"
              v-on:change="e => fetchData(chartDatum.temp_id, Number((e.target as HTMLInputElement)?.value))"
              style=" width: 230px; height: 30px; border-radius: 5px;"
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
          <button
            v-on:click.prevent="deleteGraphSettings(chartDatum.temp_id,chartDatum.id)"
            class="btn-trash-dark"
          >
            <i class="bi bi-trash"></i> <!-- ゴミ箱アイコン -->
          </button>
        </div>

      </div>
    </div>

    <!-- グラフ追加・設定保存ボタン -->
    <div class="d-flex justify-content-center">
        <button type="button" v-on:click="addChartDatum" class="custom-btn mx-1 mb-3" >グラフを追加</button>
        <button type="button" v-on:click="saveSettings" class="custom-btn mx-1 mb-3">グラフ設定を保存</button>
    </div>

  </div>
</template>



