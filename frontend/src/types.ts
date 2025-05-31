export interface TrainingRecord {
  id?: number; // 送信時は不要な場合もあるので optional にしておくと柔軟
  date: string; // "2025-04-07" のような形式なら string
  details: TrainingDetail[]; //他で定義した型を参照できる
}

export interface TrainingDetail {
  temp_id: number;
  exercise_id: number;
  weight: number;
  goal_reps: number;
  goal_sets: number;
  sets: number[];
  volume?: number;
}

export interface Exercise{
  id?: number;
  exercise_name: string;
  memo: string;
}

export interface Template{
  id?: number;
  template_name: string;
  details: TemplateDetail[];
}

export interface TemplateDetail{
  temp_id:number; //DBに保存をしIDが確定する前に詳細レコードを識別して操作を行うための暫定ID
  id?: number;
  exercise_id: number;
  exercise_name?: string ;
  weight: number;
  goal_reps: number;
  goal_sets: number;
}

export interface UserInformation{
  user_id?: number;
  user_name: string;
  password?: string;
}

export interface GraphSetting{
  id: number;
  exercise_id: number;
}