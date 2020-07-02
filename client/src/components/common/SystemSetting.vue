<template>
	<div class="system_setting_wrap">
        <v-container>
            <v-row>
                <v-col cols='8'>
                    Dark Mode
                </v-col>
                <v-col cols='4'>
                    <v-switch v-model='isDark' @change='togleDarkMode'></v-switch>
                </v-col>
            </v-row>
        </v-container>
	</div>
</template>

<script>
    import { mapState } from 'vuex'
	export default {
		name: 'SystemSetting',
        data: () => ({
            isDark: false,
        }),

		mounted: function () {
			this.$axios({
				method: 'GET',
				url: '/api/setting/'
				// url: '/api/setting/' + this.$store.state.loginUser
			})
			.then(res => {
				console.log(res)
			})
			.catch(e => {
				console.log(e)
			})
		},

		methods: {
            togleDarkMode () {
                this.$store.dispatch('settings/updateIsDark', this.isDark)
            }
        }
	}
</script>

<style lang="scss">
</style>
