new Vue({
    el: '#searchForm',
    delimiters: ['${', '}$'],
    template: '#searchFormTemplate',
    data() {
        return {
            isLoading: false,
            suggestions: [],
        }
    },
    props: {
        query: String
    },
    methods: {
        getAutoComplete: () => {
        },
        handleQueryChange: function (e) {
            const q = e.target.value;
            if (q.length == 0) {
                this.isLoading = false;
                this.suggestions = [];
            }
            if (q.length >= 2) {
                this.isLoading = true;
                this.getAutoComplete(q);
            }
        }
    },
    created() {
        this.getAutoComplete = _.debounce(async (q) => {
            const resp = await axios.get(`/api/s-suggest/sell/${q}`)
            if (resp && resp.status && resp.status == 200) {
                let suggestions = [];
                for (const item of resp.data) {
                    if (item.type == 'area') {
                        suggestions.push({
                            code: "",
                            text: "Khu vực",
                            subText: "",
                            link: "",
                            isHeader: true,
                        })
                    }
                    for (const record of item.records) {
                        suggestions.push({
                            code: record.code,
                            text: record.name,
                            subText: "",
                            link: `/listings/search?district=${record.slug}`,
                            isHeader: false,

                        })
                    }
                }
                this.suggestions = suggestions;
            }
            setTimeout(() => {
                this.isLoading = false;
            }, 200);
            return resp;
        }, 300);
    }
})