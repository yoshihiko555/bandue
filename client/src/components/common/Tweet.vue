<template>
	<v-container fluid>
		<v-row>
			<v-col cols='12'>
				<v-card
					class='mx-auto'
					max-width='400'
				>
					<v-card-title>
						<span class='title font-weight-light'>Bandue</span>
					</v-card-title>

					<v-form>
						<v-textarea
							solo
							flat
							auto-grow
							clearable
							:counter='144'
							label="何が起こっていますか？"
						></v-textarea>
						<v-file-input
						><v-icon>mdi-image</v-icon></v-file-input>
						<div class="text-right">
							<v-btn
							class='teal lighten-4 ma-3'
							>つぶやく</v-btn>
						</div>
					</v-form>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
export default {
	name: 'Tweet',
	data: () => ({

	})
}
</script>
