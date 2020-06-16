class Const {
	// サインアップページ
	SIGNUP_VIEW = 0
	SIGNUP_CONFRIM_VIEW = 1
	SIGNUP_DONE_VIEW = 2

	// 記事の種類
	ENTRY_TYPE = [
		{ text: '選択してください', value: 'NO'},
		{ text: 'Recruitment Member', value: 'RE'},
		{ text: 'Join a Group', value: 'JO'},
		{ text: 'Support', value: 'SU'},
	]

	// 都道府県
	PREFECTURE = [
		{ text: '選択してください', value: 0},
		{ text: '北海道', value: 1},
		{ text: '青森県', value: 2},
		{ text: '岩手県', value: 3},
		{ text: '宮城県', value: 4},
		{ text: '秋田県', value: 5},
		{ text: '山形県', value: 6},
		{ text: '福島県', value: 7},
		{ text: '茨城県', value: 8},
		{ text: '栃木県', value: 9},
		{ text: '群馬県', value: 10},
		{ text: '埼玉県', value: 11},
		{ text: '千葉県', value: 12},
		{ text: '東京都', value: 13},
		{ text: '神奈川県', value: 14},
		{ text: '新潟県', value: 15},
		{ text: '富山県', value: 16},
		{ text: '石川県', value: 17},
		{ text: '福井県', value: 18},
		{ text: '山梨県', value: 19},
		{ text: '長野県', value: 20},
		{ text: '岐阜県', value: 21},
		{ text: '静岡県', value: 22},
		{ text: '愛知県', value: 23},
		{ text: '三重県', value: 24},
		{ text: '滋賀県', value: 25},
		{ text: '京都府', value: 26},
		{ text: '大阪府', value: 27},
		{ text: '兵庫県', value: 28},
		{ text: '奈良県', value: 29},
		{ text: '和歌山県', value: 30},
		{ text: '鳥取県', value: 31},
		{ text: '島根県', value: 32},
		{ text: '岡山県', value: 33},
		{ text: '広島県', value: 34},
		{ text: '山口県', value: 35},
		{ text: '徳島県', value: 36},
		{ text: '香川県', value: 37},
		{ text: '愛媛県', value: 38},
		{ text: '高知県', value: 39},
		{ text: '福岡県', value: 40},
		{ text: '佐賀県', value: 41},
		{ text: '長崎県', value: 42},
		{ text: '熊本県', value: 43},
		{ text: '大分県', value: 44},
		{ text: '宮崎県', value: 45},
		{ text: '鹿児島県', value: 46},
		{ text: '沖縄県', value: 47},
	]

	// 活動の曜日
	DAY_WEEK = [
		{ text: '選択してください', value: 'NO'},
		{ text: 'Weekdays', value: 'WD'},
		{ text: 'Weekends', value: 'WE'},
		{ text: 'Always', value: 'AL'},
	]

	// 活動の方向性
	DIRECTION = [
		{ text: '選択してください', value: 'NO'},
		{ text: 'Original', value: 'OR'},
		{ text: 'Copy', value: 'CO'},
		{ text: 'All', value: 'AL'},
	]

	// 募集する性別
	SEX = [
		{ text: '選択してください', value: 0},
		{ text: 'Mail', value: 1},
		{ text: 'Famale', value: 2},
	]

	// 募集する年齢
	AGE = [
		{ text: '選択してください', value: 0},
		{ text: '~19', value: 1},
		{ text: '20~29', value: 2},
		{ text: '30~39', value: 3},
		{ text: '40~49', value: 4},
		{ text: '50~59', value: 5},
		{ text: '60~69', value: 6},
		{ text: '70~79', value: 7},
		{ text: '80~89', value: 8},
		{ text: '90~99', value: 9},
	]
}

export { Const }
