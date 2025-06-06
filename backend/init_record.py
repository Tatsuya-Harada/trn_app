from app import app,db,TrainingRecord,TrainingRecordDetail,SetReps,Exercise,Template,TemplateDetail,User,UserGraphSetting
from datetime import date
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()  # データベースを作成

    # ユーザ作成
    user1=User(username='Sample', password_hash=generate_password_hash('100') )
    db.session.add_all([user1])
    db.session.commit()

    # 種目の作成
    exercises = [
        Exercise(user_id=user1.id, name='ラテラルシャッフル', memo=''),
        Exercise(user_id=user1.id, name='ジャンプスクワット', memo=''),
        Exercise(user_id=user1.id, name='ヒップアブダクション', memo=''),
        Exercise(user_id=user1.id, name='ブルガリアンスクワット', memo=''),
        Exercise(user_id=user1.id, name='バーベルデッドリフト', memo=''),
        Exercise(user_id=user1.id, name='レッグプレス', memo=''),
        Exercise(user_id=user1.id, name='スミスマシンスクワット', memo=''),
        Exercise(user_id=user1.id, name='バーベルスクワット', memo=''),
        Exercise(user_id=user1.id, name='フォワードランジ', memo=''),
        Exercise(user_id=user1.id, name='片足スクワット', memo=''),
        Exercise(user_id=user1.id, name='バックランジ', memo=''),
        Exercise(user_id=user1.id, name='レッグカール', memo=''),
        Exercise(user_id=user1.id, name='バックエクステンション', memo=''),
        Exercise(user_id=user1.id, name='バーベルブルガリアンスクワット', memo=''),
        Exercise(user_id=user1.id, name='ルーマニアンデッドリフト', memo=''),
        Exercise(user_id=user1.id, name='ジャンプランジ', memo=''),
        Exercise(user_id=user1.id, name='ラテラルランジ', memo=''),
        Exercise(user_id=user1.id, name='ワンハンドダンベルショルダープレス', memo=''),
        Exercise(user_id=user1.id, name='アップライトロウ', memo=''),
        Exercise(user_id=user1.id, name='バーベルショルダープレス', memo=''),
        Exercise(user_id=user1.id, name='マシンショルダープレス', memo=''),
        Exercise(user_id=user1.id, name='ケーブルフライ', memo=''),
        Exercise(user_id=user1.id, name='サイドレイズ', memo=''),
        Exercise(user_id=user1.id, name='ダンベルショルダープレス', memo=''),
        Exercise(user_id=user1.id, name='スタンディングダンベルショルダープレス', memo=''),
        Exercise(user_id=user1.id, name='プッシュアップジャンプ', memo=''),
        Exercise(user_id=user1.id, name='プッシュアップ', memo=''),
        Exercise(user_id=user1.id, name='ダンベルフライ', memo=''),
        Exercise(user_id=user1.id, name='ベンチプレス', memo=''),
        Exercise(user_id=user1.id, name='チェストプレス', memo=''),
        Exercise(user_id=user1.id, name='ダンベルベンチプレス', memo=''),
        Exercise(user_id=user1.id, name='ワンハンドダンベルベンチプレス', memo=''),
        Exercise(user_id=user1.id, name='デクラインプッシュアップ', memo=''),
        Exercise(user_id=user1.id, name='マシンフライ', memo=''),
        Exercise(user_id=user1.id, name='ワイドプッシュアップ', memo=''),
        Exercise(user_id=user1.id, name='アーチャープッシュアップ', memo=''),
        Exercise(user_id=user1.id, name='ケーブルフライ', memo=''),
        Exercise(user_id=user1.id, name='インクラインダンベルベンチプレス', memo=''),
        Exercise(user_id=user1.id, name='フロアダンベルベンチプレス', memo=''),
        Exercise(user_id=user1.id, name='ツイストプッシュアップ', memo=''),
        Exercise(user_id=user1.id, name='ナロー&ワイドプッシュアップ', memo=''),
        Exercise(user_id=user1.id, name='フロアダンベルフライ', memo=''),
        Exercise(user_id=user1.id, name='インクラインマシンプレス', memo=''),
        Exercise(user_id=user1.id, name='インクラインプッシュアップ', memo=''),
        Exercise(user_id=user1.id, name='マシンベンチプレス', memo=''),
        Exercise(user_id=user1.id, name='シーテッドロウ', memo=''),
        Exercise(user_id=user1.id, name='ダンベルベントオーバーロウ', memo=''),
        Exercise(user_id=user1.id, name='ベントオーバーローイング', memo=''),
        Exercise(user_id=user1.id, name='ラットプルダウン', memo=''),
        Exercise(user_id=user1.id, name='ワンハンドダンベルロウ', memo=''),
        Exercise(user_id=user1.id, name='プルオーバー', memo=''),
        Exercise(user_id=user1.id, name='バーベルベントオーバーロウ', memo=''),
        Exercise(user_id=user1.id, name='バックエクステンション', memo=''),
        Exercise(user_id=user1.id, name='ダンベルロウ', memo=''),
        Exercise(user_id=user1.id, name='リバースフライ', memo=''),
        Exercise(user_id=user1.id, name='チンニング', memo=''),
        Exercise(user_id=user1.id, name='シーテッドロウ', memo=''),
    ]
    db.session.add_all(exercises)
    db.session.commit()

    # レコードの作成
    record = [
        TrainingRecord(user_id=1, date=date(2023, 1, 11)),   # 2023/1/11
        TrainingRecord(user_id=1, date=date(2023, 1, 14)),   # 2023/1/14
        TrainingRecord(user_id=1, date=date(2023, 1, 24)),   # 2023/1/24
        TrainingRecord(user_id=1, date=date(2023, 1, 27)),   # 2023/1/27
        TrainingRecord(user_id=1, date=date(2023, 2, 9)),    # 2023/2/9
        TrainingRecord(user_id=1, date=date(2023, 2, 14)),   # 2023/2/14
        TrainingRecord(user_id=1, date=date(2023, 2, 17)),   # 2023/2/17
        TrainingRecord(user_id=1, date=date(2023, 2, 24)),   # 2023/2/24
        TrainingRecord(user_id=1, date=date(2023, 2, 27)),   # 2023/2/27
        TrainingRecord(user_id=1, date=date(2023, 3, 7)),    # 2023/3/7
        TrainingRecord(user_id=1, date=date(2023, 3, 9)),    # 2023/3/9
        TrainingRecord(user_id=1, date=date(2023, 3, 13)),   # 2023/3/13
        TrainingRecord(user_id=1, date=date(2023, 3, 28)),   # 2023/3/28
        TrainingRecord(user_id=1, date=date(2023, 4, 4)),    # 2023/4/4
        TrainingRecord(user_id=1, date=date(2023, 4, 14)),   # 2023/4/14
        TrainingRecord(user_id=1, date=date(2023, 4, 18)),   # 2023/4/18
        TrainingRecord(user_id=1, date=date(2023, 4, 28)),   # 2023/4/28
        TrainingRecord(user_id=1, date=date(2023, 5, 13)),   # 2023/5/13
        TrainingRecord(user_id=1, date=date(2023, 5, 18)),   # 2023/5/18
        TrainingRecord(user_id=1, date=date(2023, 5, 30)),   # 2023/5/30
        TrainingRecord(user_id=1, date=date(2023, 6, 2)),    # 2023/6/2
        TrainingRecord(user_id=1, date=date(2023, 6, 20)),   # 2023/6/20
        TrainingRecord(user_id=1, date=date(2023, 6, 23)),   # 2023/6/23
        TrainingRecord(user_id=1, date=date(2023, 7, 4)),    # 2023/7/4
        TrainingRecord(user_id=1, date=date(2023, 7, 10)),   # 2023/7/10
        TrainingRecord(user_id=1, date=date(2023, 7, 21)),   # 2023/7/21
        TrainingRecord(user_id=1, date=date(2023, 7, 24)),   # 2023/7/24
        TrainingRecord(user_id=1, date=date(2023, 8, 4)),    # 2023/8/4
        TrainingRecord(user_id=1, date=date(2023, 8, 9)),    # 2023/8/9
        TrainingRecord(user_id=1, date=date(2023, 8, 22)),   # 2023/8/22
        TrainingRecord(user_id=1, date=date(2023, 8, 25)),   # 2023/8/25
        TrainingRecord(user_id=1, date=date(2023, 9, 11)),   # 2023/9/11
        TrainingRecord(user_id=1, date=date(2023, 9, 14)),   # 2023/9/14
        TrainingRecord(user_id=1, date=date(2023, 9, 26)),   # 2023/9/26
        TrainingRecord(user_id=1, date=date(2023, 9, 28)),   # 2023/9/28
        TrainingRecord(user_id=1, date=date(2023, 10, 13)),  # 2023/10/13
        TrainingRecord(user_id=1, date=date(2023, 10, 19)),  # 2023/10/19
        TrainingRecord(user_id=1, date=date(2023, 10, 29)),  # 2023/10/29
        TrainingRecord(user_id=1, date=date(2023, 11, 3)),   # 2023/11/3
        TrainingRecord(user_id=1, date=date(2023, 11, 14)),  # 2023/11/14
        TrainingRecord(user_id=1, date=date(2023, 11, 17)),  # 2023/11/17
        TrainingRecord(user_id=1, date=date(2023, 11, 28)),  # 2023/11/28
        TrainingRecord(user_id=1, date=date(2023, 12, 2)),   # 2023/12/2
        TrainingRecord(user_id=1, date=date(2023, 12, 9)),   # 2023/12/9
        TrainingRecord(user_id=1, date=date(2023, 12, 16)),  # 2023/12/16
        TrainingRecord(user_id=1, date=date(2024, 1, 7)),   # 2024/1/7
        TrainingRecord(user_id=1, date=date(2024, 1, 14)),  # 2024/1/14
        TrainingRecord(user_id=1, date=date(2024, 2, 4)),   # 2024/2/4
        TrainingRecord(user_id=1, date=date(2024, 2, 10)),  # 2024/2/10
        TrainingRecord(user_id=1, date=date(2024, 2, 29)),  # 2024/2/29
        TrainingRecord(user_id=1, date=date(2024, 3, 3)),   # 2024/3/3
        TrainingRecord(user_id=1, date=date(2024, 3, 23)),  # 2024/3/23
        TrainingRecord(user_id=1, date=date(2024, 4, 6)),   # 2024/4/6
        TrainingRecord(user_id=1, date=date(2024, 5, 5)),   # 2024/5/5
        TrainingRecord(user_id=1, date=date(2024, 5, 12)),  # 2024/5/12
        TrainingRecord(user_id=1, date=date(2024, 6, 2)),   # 2024/6/2
        TrainingRecord(user_id=1, date=date(2024, 6, 9)),   # 2024/6/9
        TrainingRecord(user_id=1, date=date(2024, 6, 29)),  # 2024/6/29
        TrainingRecord(user_id=1, date=date(2024, 7, 7)),   # 2024/7/7
        TrainingRecord(user_id=1, date=date(2024, 8, 4)),   # 2024/8/4
        TrainingRecord(user_id=1, date=date(2024, 8, 14)),  # 2024/8/14
        TrainingRecord(user_id=1, date=date(2024, 8, 30)),  # 2024/8/30
        TrainingRecord(user_id=1, date=date(2024, 9, 8)),   # 2024/9/8
        TrainingRecord(user_id=1, date=date(2024, 9, 30)),  # 2024/9/30
        TrainingRecord(user_id=1, date=date(2024, 10, 6)),  # 2024/10/6
        TrainingRecord(user_id=1, date=date(2024, 11, 2)),  # 2024/11/2
        TrainingRecord(user_id=1, date=date(2024, 11, 17)), # 2024/11/17
        TrainingRecord(user_id=1, date=date(2024, 12, 28)), # 2024/12/28
        TrainingRecord(user_id=1, date=date(2025, 2, 14)),  # 2025/2/14
    ]

    db.session.add_all(record)
    db.session.commit()

    # レコード詳細
    record_detail = [
        # 2023/1/11 マシンベンチプレス
        TrainingRecordDetail(record_id=record[0].id, exercise_id=exercises[44].id, weight=78, volume=1716),
        # 2023/1/11 ラットプルダウン
        TrainingRecordDetail(record_id=record[0].id, exercise_id=exercises[48].id, weight=57, volume=1311),
        # 2023/1/11 バーベルスクワット
        TrainingRecordDetail(record_id=record[0].id, exercise_id=exercises[7].id, weight=110, volume=2310),
        # 2023/1/14 ラットプルダウン
        TrainingRecordDetail(record_id=record[1].id, exercise_id=exercises[48].id, weight=52, volume=1664),
        # 2023/1/14 マシンベンチプレス
        TrainingRecordDetail(record_id=record[1].id, exercise_id=exercises[44].id, weight=71, volume=1988),
        # 2023/1/24 マシンベンチプレス
        TrainingRecordDetail(record_id=record[2].id, exercise_id=exercises[44].id, weight=78, volume=1560),
        # 2023/1/24 ラットプルダウン
        TrainingRecordDetail(record_id=record[2].id, exercise_id=exercises[48].id, weight=57, volume=1368),
        # 2023/1/24 バーベルスクワット
        TrainingRecordDetail(record_id=record[2].id, exercise_id=exercises[7].id, weight=110, volume=2530),
        # 2023/1/27 ラットプルダウン
        TrainingRecordDetail(record_id=record[3].id, exercise_id=exercises[48].id, weight=52, volume=1768),
        # 2023/1/27 マシンベンチプレス
        TrainingRecordDetail(record_id=record[3].id, exercise_id=exercises[44].id, weight=71, volume=2130),
        # 2023/1/27 バーベルスクワット
        TrainingRecordDetail(record_id=record[3].id, exercise_id=exercises[7].id, weight=100, volume=3200),
        # 2023/2/9 ラットプルダウン
        TrainingRecordDetail(record_id=record[4].id, exercise_id=exercises[48].id, weight=57, volume=1368),
        # 2023/2/9 マシンベンチプレス
        TrainingRecordDetail(record_id=record[4].id, exercise_id=exercises[44].id, weight=78, volume=1638),
        # 2023/2/14 ラットプルダウン
        TrainingRecordDetail(record_id=record[5].id, exercise_id=exercises[48].id, weight=52, volume=1768),
        # 2023/2/14 マシンベンチプレス
        TrainingRecordDetail(record_id=record[5].id, exercise_id=exercises[44].id, weight=71, volume=2130),
        # 2023/2/17 バーベルスクワット
        TrainingRecordDetail(record_id=record[6].id, exercise_id=exercises[7].id, weight=100, volume=3400),
        # 2023/2/24 ラットプルダウン
        TrainingRecordDetail(record_id=record[7].id, exercise_id=exercises[48].id, weight=62, volume=1178),
        # 2023/2/24 マシンベンチプレス
        TrainingRecordDetail(record_id=record[7].id, exercise_id=exercises[44].id, weight=78, volume=1872),
        # 2023/2/27 ラットプルダウン
        TrainingRecordDetail(record_id=record[8].id, exercise_id=exercises[48].id, weight=52, volume=1820),
        # 2023/2/27 マシンベンチプレス
        TrainingRecordDetail(record_id=record[8].id, exercise_id=exercises[44].id, weight=71, volume=2201),
        # 2023/2/27 バーベルスクワット
        TrainingRecordDetail(record_id=record[8].id, exercise_id=exercises[7].id, weight=100, volume=3300),
        # 2023/3/7 ラットプルダウン
        TrainingRecordDetail(record_id=record[9].id, exercise_id=exercises[48].id, weight=47, volume=1363),
        # 2023/3/9 ラットプルダウン
        TrainingRecordDetail(record_id=record[10].id, exercise_id=exercises[48].id, weight=62, volume=1240),
        # 2023/3/9 マシンベンチプレス
        TrainingRecordDetail(record_id=record[10].id, exercise_id=exercises[44].id, weight=80.5, volume=1529.5),
        # 2023/3/13 ラットプルダウン
        TrainingRecordDetail(record_id=record[11].id, exercise_id=exercises[48].id, weight=57, volume=1596),
        # 2023/3/13 マシンベンチプレス
        TrainingRecordDetail(record_id=record[11].id, exercise_id=exercises[44].id, weight=73.5, volume=1984.5),
        # 2023/3/13 バーベルスクワット
        TrainingRecordDetail(record_id=record[11].id, exercise_id=exercises[7].id, weight=100, volume=3400),
        # 2023/3/28 マシンベンチプレス
        TrainingRecordDetail(record_id=record[12].id, exercise_id=exercises[44].id, weight=80.5, volume=1610),
        # 2023/3/28 ラットプルダウン
        TrainingRecordDetail(record_id=record[12].id, exercise_id=exercises[48].id, weight=62, volume=1302),
        # 2023/3/28 バーベルスクワット
        TrainingRecordDetail(record_id=record[12].id, exercise_id=exercises[7].id, weight=110, volume=2640),
        # 2023/4/4 ラットプルダウン
        TrainingRecordDetail(record_id=record[13].id, exercise_id=exercises[48].id, weight=57, volume=1539),
        # 2023/4/14 バーベルスクワット
        TrainingRecordDetail(record_id=record[14].id, exercise_id=exercises[7].id, weight=115, volume=2530),
        # 2023/4/14 ラットプルダウン
        TrainingRecordDetail(record_id=record[14].id, exercise_id=exercises[48].id, weight=62, volume=1364),
        # 2023/4/18 ラットプルダウン
        TrainingRecordDetail(record_id=record[15].id, exercise_id=exercises[48].id, weight=57, volume=1425),
        # 2023/4/28 バーベルスクワット
        TrainingRecordDetail(record_id=record[16].id, exercise_id=exercises[7].id, weight=115, volume=2645),
        # 2023/4/28 マシンベンチプレス
        TrainingRecordDetail(record_id=record[16].id, exercise_id=exercises[44].id, weight=80.5, volume=1610),
        # 2023/5/13 マシンベンチプレス
        TrainingRecordDetail(record_id=record[17].id, exercise_id=exercises[44].id, weight=80.5, volume=1771),
        # 2023/5/13 バーベルスクワット
        TrainingRecordDetail(record_id=record[17].id, exercise_id=exercises[7].id, weight=120, volume=2160),
        # 2023/5/18 バーベルスクワット
        TrainingRecordDetail(record_id=record[18].id, exercise_id=exercises[7].id, weight=105, volume=3045),
        # 2023/5/18 マシンベンチプレス
        TrainingRecordDetail(record_id=record[18].id, exercise_id=exercises[44].id, weight=73.5, volume=2058),
        # 2023/5/30 マシンベンチプレス
        TrainingRecordDetail(record_id=record[19].id, exercise_id=exercises[44].id, weight=80.5, volume=1368.5),
        # 2023/5/30 バーベルスクワット
        TrainingRecordDetail(record_id=record[19].id, exercise_id=exercises[7].id, weight=120, volume=2280),
        # 2023/6/2 バーベルスクワット
        TrainingRecordDetail(record_id=record[20].id, exercise_id=exercises[7].id, weight=105, volume=3045),
        # 2023/6/2 マシンベンチプレス
        TrainingRecordDetail(record_id=record[20].id, exercise_id=exercises[44].id, weight=73.5, volume=2058),
        # 2023/6/20 マシンベンチプレス
        TrainingRecordDetail(record_id=record[21].id, exercise_id=exercises[44].id, weight=80.5, volume=1610),
        # 2023/6/23 マシンベンチプレス
        TrainingRecordDetail(record_id=record[22].id, exercise_id=exercises[44].id, weight=73.5, volume=1911),
        # 2023/7/4 マシンベンチプレス
        TrainingRecordDetail(record_id=record[23].id, exercise_id=exercises[44].id, weight=80.5, volume=1529.5),
        # 2023/7/4 バーベルスクワット
        TrainingRecordDetail(record_id=record[23].id, exercise_id=exercises[7].id, weight=120, volume=1200),
        # 2023/7/10 ラットプルダウン
        TrainingRecordDetail(record_id=record[24].id, exercise_id=exercises[48].id, weight=57, volume=1767),
        # 2023/7/10 マシンベンチプレス
        TrainingRecordDetail(record_id=record[24].id, exercise_id=exercises[44].id, weight=73.5, volume=2058),
        # 2023/7/21 バーベルスクワット
        TrainingRecordDetail(record_id=record[25].id, exercise_id=exercises[7].id, weight=120, volume=2160),
        # 2023/7/21 マシンベンチプレス
        TrainingRecordDetail(record_id=record[25].id, exercise_id=exercises[44].id, weight=80.5, volume=1529.5),
        # 2023/7/24 ラットプルダウン
        TrainingRecordDetail(record_id=record[26].id, exercise_id=exercises[48].id, weight=57, volume=1710),
        # 2023/7/24 マシンベンチプレス
        TrainingRecordDetail(record_id=record[26].id, exercise_id=exercises[44].id, weight=73.5, volume=1984.5),
        # 2023/7/24 バーベルスクワット
        TrainingRecordDetail(record_id=record[26].id, exercise_id=exercises[7].id, weight=105, volume=2625),
        # 2023/8/4 バーベルスクワット
        TrainingRecordDetail(record_id=record[27].id, exercise_id=exercises[7].id, weight=120, volume=2160),
        # 2023/8/4 マシンベンチプレス
        TrainingRecordDetail(record_id=record[27].id, exercise_id=exercises[44].id, weight=80.5, volume=1690.5),
        # 2023/8/9 ラットプルダウン
        TrainingRecordDetail(record_id=record[28].id, exercise_id=exercises[48].id, weight=57, volume=1482),
        # 2023/8/9 マシンベンチプレス
        TrainingRecordDetail(record_id=record[28].id, exercise_id=exercises[44].id, weight=73.5, volume=1911),
        # 2023/8/22 マシンベンチプレス
        TrainingRecordDetail(record_id=record[29].id, exercise_id=exercises[44].id, weight=80.5, volume=1529.5),
        # 2023/8/25 ラットプルダウン
        TrainingRecordDetail(record_id=record[30].id, exercise_id=exercises[48].id, weight=55, volume=1705),
        # 2023/8/25 バーベルスクワット
        TrainingRecordDetail(record_id=record[30].id, exercise_id=exercises[7].id, weight=105, volume=2940),
        # 2023/9/11 マシンベンチプレス
        TrainingRecordDetail(record_id=record[31].id, exercise_id=exercises[44].id, weight=80.5, volume=1449),
        # 2023/9/11 バーベルスクワット
        TrainingRecordDetail(record_id=record[31].id, exercise_id=exercises[7].id, weight=120, volume=2040),
        # 2023/9/14 マシンベンチプレス
        TrainingRecordDetail(record_id=record[32].id, exercise_id=exercises[44].id, weight=73.5, volume=1984.5),
        # 2023/9/14 ラットプルダウン
        TrainingRecordDetail(record_id=record[32].id, exercise_id=exercises[48].id, weight=57, volume=1596),
        # 2023/9/26 マシンベンチプレス
        TrainingRecordDetail(record_id=record[33].id, exercise_id=exercises[44].id, weight=80.5, volume=1449),
        # 2023/9/28 マシンベンチプレス
        TrainingRecordDetail(record_id=record[34].id, exercise_id=exercises[44].id, weight=73.5, volume=1984.5),
        # 2023/9/28 ラットプルダウン
        TrainingRecordDetail(record_id=record[34].id, exercise_id=exercises[48].id, weight=57, volume=1596),
        # 2023/9/28 バーベルスクワット
        TrainingRecordDetail(record_id=record[34].id, exercise_id=exercises[7].id, weight=105, volume=3255),
        # 2023/10/13 マシンベンチプレス
        TrainingRecordDetail(record_id=record[35].id, exercise_id=exercises[44].id, weight=80.5, volume=1771),
        # 2023/10/19 ラットプルダウン
        TrainingRecordDetail(record_id=record[36].id, exercise_id=exercises[48].id, weight=57, volume=1653),
        # 2023/10/19 マシンベンチプレス
        TrainingRecordDetail(record_id=record[36].id, exercise_id=exercises[44].id, weight=73.5, volume=2205),
        # 2023/10/19 バーベルスクワット
        TrainingRecordDetail(record_id=record[36].id, exercise_id=exercises[7].id, weight=105, volume=3360),
        # 2023/10/29 マシンベンチプレス
        TrainingRecordDetail(record_id=record[37].id, exercise_id=exercises[44].id, weight=80.5, volume=1851.5),
        # 2023/10/29 ラットプルダウン
        TrainingRecordDetail(record_id=record[37].id, exercise_id=exercises[48].id, weight=47, volume=1410),
        # 2023/11/3 バーベルスクワット
        TrainingRecordDetail(record_id=record[38].id, exercise_id=exercises[7].id, weight=105, volume=3465),
        # 2023/11/3 ラットプルダウン
        TrainingRecordDetail(record_id=record[38].id, exercise_id=exercises[48].id, weight=57, volume=1767),
        # 2023/11/3 マシンベンチプレス
        TrainingRecordDetail(record_id=record[38].id, exercise_id=exercises[44].id, weight=73.5, volume=2278.5),
        # 2023/11/14 マシンベンチプレス
        TrainingRecordDetail(record_id=record[39].id, exercise_id=exercises[44].id, weight=80.5, volume=1851.5),
        # 2023/11/17 ラットプルダウン
        TrainingRecordDetail(record_id=record[40].id, exercise_id=exercises[48].id, weight=57, volume=1881),
        # 2023/11/17 マシンベンチプレス
        TrainingRecordDetail(record_id=record[40].id, exercise_id=exercises[44].id, weight=73.5, volume=2352),
        # 2023/11/28 バーベルスクワット
        TrainingRecordDetail(record_id=record[41].id, exercise_id=exercises[7].id, weight=120, volume=2520),
        # 2023/11/28 マシンベンチプレス
        TrainingRecordDetail(record_id=record[41].id, exercise_id=exercises[44].id, weight=80.5, volume=1851.5),
        # 2023/12/2 ラットプルダウン
        TrainingRecordDetail(record_id=record[42].id, exercise_id=exercises[48].id, weight=57, volume=1995),
        # 2023/12/2 マシンベンチプレス
        TrainingRecordDetail(record_id=record[42].id, exercise_id=exercises[44].id, weight=73.5, volume=2352),
        # 2023/12/9 バーベルスクワット
        TrainingRecordDetail(record_id=record[43].id, exercise_id=exercises[7].id, weight=120, volume=2400),
        # 2023/12/16 ラットプルダウン
        TrainingRecordDetail(record_id=record[44].id, exercise_id=exercises[48].id, weight=57, volume=1995),
        # 2023/12/16 マシンベンチプレス
        TrainingRecordDetail(record_id=record[44].id, exercise_id=exercises[44].id, weight=73.5, volume=2499),
        # 2023/12/16 バーベルスクワット
        TrainingRecordDetail(record_id=record[44].id, exercise_id=exercises[7].id, weight=105, volume=3255),
        # 2024/1/7 マシンベンチプレス
        TrainingRecordDetail(record_id=record[45].id, exercise_id=exercises[44].id, weight=80.5, volume=1932),
        # 2024/1/14 ラットプルダウン
        TrainingRecordDetail(record_id=record[46].id, exercise_id=exercises[48].id, weight=62, volume=1674),
        # 2024/1/14 マシンベンチプレス
        TrainingRecordDetail(record_id=record[46].id, exercise_id=exercises[44].id, weight=73.5, volume=2131.5),
        # 2024/2/4 マシンベンチプレス
        TrainingRecordDetail(record_id=record[47].id, exercise_id=exercises[44].id, weight=80.5, volume=1771),
        # 2024/2/10 バーベルスクワット
        TrainingRecordDetail(record_id=record[48].id, exercise_id=exercises[7].id, weight=105, volume=3780),
        # 2024/2/10 ラットプルダウン
        TrainingRecordDetail(record_id=record[48].id, exercise_id=exercises[48].id, weight=62, volume=1736),
        # 2024/2/10 マシンベンチプレス
        TrainingRecordDetail(record_id=record[48].id, exercise_id=exercises[44].id, weight=73.5, volume=2352),
        # 2024/2/29 バーベルスクワット
        TrainingRecordDetail(record_id=record[49].id, exercise_id=exercises[7].id, weight=120, volume=2760),
        # 2024/2/29 マシンベンチプレス
        TrainingRecordDetail(record_id=record[49].id, exercise_id=exercises[44].id, weight=80.5, volume=1932),
        # 2024/3/3 バーベルスクワット
        TrainingRecordDetail(record_id=record[50].id, exercise_id=exercises[7].id, weight=110, volume=3190),
        # 2024/3/3 マシンベンチプレス
        TrainingRecordDetail(record_id=record[50].id, exercise_id=exercises[44].id, weight=73.5, volume=2205),
        # 2024/3/23 マシンベンチプレス
        TrainingRecordDetail(record_id=record[51].id, exercise_id=exercises[44].id, weight=83, volume=1826),
        # 2024/3/23 バーベルスクワット
        TrainingRecordDetail(record_id=record[51].id, exercise_id=exercises[7].id, weight=125, volume=1625),
        # 2024/4/6 マシンベンチプレス
        TrainingRecordDetail(record_id=record[52].id, exercise_id=exercises[44].id, weight=73.5, volume=2278.5),
        # 2024/4/6 バーベルスクワット
        TrainingRecordDetail(record_id=record[52].id, exercise_id=exercises[7].id, weight=110, volume=2200),
        # 2024/5/5 マシンベンチプレス
        TrainingRecordDetail(record_id=record[53].id, exercise_id=exercises[44].id, weight=83, volume=1743),
        # 2024/5/12 マシンベンチプレス
        TrainingRecordDetail(record_id=record[54].id, exercise_id=exercises[44].id, weight=73.5, volume=2131.5),
        # 2024/6/2 マシンベンチプレス
        TrainingRecordDetail(record_id=record[55].id, exercise_id=exercises[44].id, weight=83, volume=1826),
        # 2024/6/9 バーベルスクワット
        TrainingRecordDetail(record_id=record[56].id, exercise_id=exercises[7].id, weight=110, volume=3410),
        # 2024/6/9 マシンベンチプレス
        TrainingRecordDetail(record_id=record[56].id, exercise_id=exercises[44].id, weight=73.5, volume=1837.5),
        # 2024/6/29 マシンベンチプレス
        TrainingRecordDetail(record_id=record[57].id, exercise_id=exercises[44].id, weight=83, volume=1660),
        # 2024/6/29 バーベルスクワット
        TrainingRecordDetail(record_id=record[57].id, exercise_id=exercises[7].id, weight=125, volume=2125),
        # 2024/7/7 マシンベンチプレス
        TrainingRecordDetail(record_id=record[58].id, exercise_id=exercises[44].id, weight=73.5, volume=2131.5),
        # 2024/8/4 ラットプルダウン
        TrainingRecordDetail(record_id=record[59].id, exercise_id=exercises[48].id, weight=62, volume=1488),
        # 2024/8/4 マシンベンチプレス
        TrainingRecordDetail(record_id=record[59].id, exercise_id=exercises[44].id, weight=84, volume=1680),
        # 2024/8/14 マシンベンチプレス
        TrainingRecordDetail(record_id=record[60].id, exercise_id=exercises[44].id, weight=73.5, volume=1911),
        # 2024/8/30 マシンベンチプレス
        TrainingRecordDetail(record_id=record[61].id, exercise_id=exercises[44].id, weight=84, volume=1764),
        # 2024/9/8 マシンベンチプレス
        TrainingRecordDetail(record_id=record[62].id, exercise_id=exercises[44].id, weight=73.5, volume=2131.5),
        # 2024/9/30 バーベルスクワット
        TrainingRecordDetail(record_id=record[63].id, exercise_id=exercises[7].id, weight=125, volume=1750),
        # 2024/10/6 マシンベンチプレス
        TrainingRecordDetail(record_id=record[64].id, exercise_id=exercises[44].id, weight=73.5, volume=2278.5),
        # 2024/11/2 ラットプルダウン
        TrainingRecordDetail(record_id=record[65].id, exercise_id=exercises[48].id, weight=65, volume=1560),
        # 2024/11/17 マシンベンチプレス
        TrainingRecordDetail(record_id=record[66].id, exercise_id=exercises[44].id, weight=73.5, volume=2131.5),
        # 2024/12/28 マシンベンチプレス
        TrainingRecordDetail(record_id=record[67].id, exercise_id=exercises[44].id, weight=84, volume=1428),
        # 2025/2/14 マシンベンチプレス
        TrainingRecordDetail(record_id=record[68].id, exercise_id=exercises[44].id, weight=84, volume=1848),
        # 2025/2/14 ラットプルダウン
        TrainingRecordDetail(record_id=record[68].id, exercise_id=exercises[48].id, weight=62, volume=1426),
        
    ]

    db.session.add_all(record_detail)
    db.session.commit() 

    # テンプレート
    template=[
        Template(user_id=user1.id,name='全身トレーニング_ハイレップ'),
        Template(user_id=user1.id,name='全身トレーニング_ローレップ')
    ]

    db.session.add_all(template)
    db.session.commit() 

    # テンプレート詳細
    template_detail=[
        TemplateDetail(template_id=template[0].id, exercise_id=exercises[48].id, weight=52, goal_reps=16, goal_sets=3),
        TemplateDetail(template_id=template[0].id, exercise_id=exercises[44].id, weight=66, goal_reps=15, goal_sets=3),
        TemplateDetail(template_id=template[0].id, exercise_id=exercises[56].id, weight=62, goal_reps=15, goal_sets=3),
        TemplateDetail(template_id=template[0].id, exercise_id=exercises[7].id, weight=100, goal_reps=15, goal_sets=3),
        TemplateDetail(template_id=template[0].id, exercise_id=exercises[20].id, weight=39, goal_reps=15, goal_sets=3),
        TemplateDetail(template_id=template[1].id, exercise_id=exercises[48].id, weight=72, goal_reps=6, goal_sets=5),
        TemplateDetail(template_id=template[1].id, exercise_id=exercises[44].id, weight=91, goal_reps=6, goal_sets=5),
        TemplateDetail(template_id=template[1].id, exercise_id=exercises[56].id, weight=95, goal_reps=6, goal_sets=4)
    ]

    db.session.add_all(template_detail)
    db.session.commit() 

    # 表示グラフ設定
    graph_setting=[
        UserGraphSetting(user_id=user1.id,exercise_id=exercises[7],order=1),
        UserGraphSetting(user_id=user1.id,exercise_id=exercises[48],order=1)
    ]
  


    #ユーザ作成
    # user1=User(username='test1', password_hash=generate_password_hash('111') )
    # db.session.add_all([user1])
    # db.session.commit()

    # #種目の作成
    # exercise1=Exercise(user_id=user1.id, name='ベンチプレス', memo='肩幅よりも少し広めに握る')
    # exercise2=Exercise(user_id=user1.id, name='スクワット', memo='最大可動域で行う')
    # exercise3=Exercise(user_id=user1.id, name='デッドリフト', memo='背中を曲げない')
    # db.session.add_all([exercise1,exercise2,exercise3])
    # db.session.commit()

    # #レコードの作成
    # record=[
    #     TrainingRecord(user_id=user1.id, date=date(2025,1,1)),
    #     TrainingRecord(user_id=user1.id, date=date(2025,2,1))
    # ]
    # db.session.add_all(record)
    # db.session.commit()

    # # レコード詳細
    # record1_detail=[
    #     TrainingRecordDetail(record_id=record[0].id, exercise_id=exercise1.id, weight=80, volume=1600),
    #     TrainingRecordDetail(record_id=record[0].id, exercise_id=exercise2.id, weight=100, volume=2000 ),
    #     TrainingRecordDetail(record_id=record[1].id, exercise_id=exercise1.id, weight=100, volume=2500),
    #     TrainingRecordDetail(record_id=record[1].id, exercise_id=exercise2.id, weight=500, volume=1800),
    # ]
    # db.session.add_all(record1_detail)
    # db.session.commit()

    # セットごとのレップ数
    # record_detail_reps=[
    #     SetReps(detail_id=record1_detail[0].id,set_number=1,reps=12),
    #     SetReps(detail_id=record1_detail[0].id,set_number=2,reps=10),
    #     SetReps(detail_id=record1_detail[0].id,set_number=3,reps=8)
    #    ]

    # # テンプレート
    # template1=Template(user_id=user1.id,name='サンプルテンプレート1')
    # template2=Template(user_id=user1.id,name='サンプルテンプレート2')
    # template1_detail1=TemplateDetail(template_id=1, exercise_id=exercise1.id, weight=10, goal_reps=3, goal_sets=3)
    # db.session.add_all([template1,template2,template1_detail1])
    # db.session.commit()