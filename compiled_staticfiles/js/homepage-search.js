new Vue({
    el: '#searchFormHome',
    delimiters: ['${', '}$'],
    template: '#searchFormTemplate',
    data() {
        return {
            isLoading: false,
            isFocus: false,
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
        },
        handleFocus: function (e) {
            this.isFocus = !this.isFocus;
        },
        setupAutoComplete: function () {
            clearInterval(this.interval);
            const getHeaderText = (itemType) => {
                switch (itemType) {
                    case 'area':
                        return 'Khu vực';
                    case 'street':
                        return 'Đường';
                    case 'urban_area':
                        return 'Khu dân cư'
                    default:
                        return 'Khu vực'
                }
            }

            this.getAutoComplete = _.debounce(async (q) => {
                const resp = await axios.get(`/api/s-suggest/sell/${q}`)
                if (resp && resp.status && resp.status == 200) {
                    let suggestions = [];
                    let headers = {};
                    for (const item of resp.data) {

                        if (!(item.type in headers)) {
                            suggestions.push({
                                code: item.id,
                                text: getHeaderText(item.type),
                                subText: item.text,
                                link: "",
                                isHeader: true,
                            })
                            headers[item.type] = 1
                        }
                        if (item.sub_type !== 'state') {
                            suggestions.push({
                                code: item.id,
                                text: item.text,
                                subText: item.text,
                                link: `/listings/search?trans=${item.type}&keys=${item.text}`,
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
        },
    },
    created() {
       this.interval = setInterval(() => {
           if (window._ && axios) {
               this.setupAutoComplete();
           }
       }, 100)
    }
})