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

            <v-row>
                <v-card :dark='this.$store.state.settings.isDark'>
                    <v-card-title>TITLE</v-card-title>
                    <v-card-text>CONTENT</v-card-text>

                </v-card>
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

		},

		methods: {
            togleDarkMode () {
                this.$store.dispatch('settings/updateIsDark')
            }
        }
	}
</script>

<style lang="scss">
</style>
