<template>
	<div class="system_setting_wrap">
        <v-container>
            <v-row>
                <v-col cols='8'>
                    Dark Mode
                </v-col>
                <v-col cols='4'>
                    <v-switch v-model='settingData.isDark' @change='toggleDarkMode'></v-switch>
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
            settingData: {
                isDark: false,
            },
        }),

		mounted: function () {
			const loginUser = this.$store.state.loginUser
			this.$axios.get('/api/profile/' + loginUser + '/')
			.then(res => {
                console.log(res)
                this.settingData = res.data.setting
			})
			.catch(e => {
				console.log(e.response)
			})
		},

		methods: {
            toggleDarkMode () {
                this.$axios({
                    url: '/api/setting/' + this.settingData.id + '/',
                    method: 'PUT',
                    data: this.settingData
                })
                .then(res => {
                    console.log(res)
                    this.$store.dispatch('settings/updateIsDark', this.settingData.isDark)
                })
                .catch(e => {
                    console.log(e)
                })
            }
        }
	}
</script>

<style lang="scss">
</style>
