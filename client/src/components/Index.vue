<template>
	<v-app>
		<p v-if='isAuth'>ログイン済み</p>
		<div v-for='data in datas' :key='data.author'>
			{{ data.author }}
			{{ data.content }}
			{{ data.liked }}
			{{ data.hashTag }}
			{{ data.created_at }}
			{{ data.updated_at }}
		</div>

		<p v-if='!isAuth'>ログインして</p>
	</v-app>
</template>

<script>
export default {
  name: 'Index',
  props: ['datas', 'isAuth'],
  data: () => ({

  })
}
</script>
