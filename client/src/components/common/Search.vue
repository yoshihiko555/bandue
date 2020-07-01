<template>
	<v-card
		flat
        :dark='this.$store.state.settings.isDark'
	>
		<v-text-field
			prepend-inner-icon='mdi-magnify'
			v-model='searchText'
		>
		</v-text-field>
		<component :is='currentView' :search-text=searchText></component>
	</v-card>
</template>

<script>
import News from '@/components/common/News'
import SearchResult from '@/components/common/SearchResult'

export default {
	name: 'Search',
	components: {
		News,
		SearchResult,
	},
	data: () => ({
		currentView: 'News',
		searchText: ''
	}),
	computed: {

	},
	watch: {
		searchText: function(val) {
			if (val.length > 0) {
				this.currentView = 'SearchResult'
			} else {
				this.currentView = 'News'
			}
		}
	},
	created () {

	},
	mounted: function () {

	},
	methods: {
		
	}
}
</script>
