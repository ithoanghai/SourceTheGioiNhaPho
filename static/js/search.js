new Vue({
    el: '#topSearchForm',
    // delimiters: ["[[", "]]"],
    delimiters: ['${', '}$'],
    template: '#topSearchTemplate',
    data() {
        return {
            isLoading: false,
            isFocus: false,
            suggestions: [],
            query: '',
        }
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

const ContactPopUpComponent = Vue.extend({
    template: '#contactPopupTemplate',
    delimiters: ["[[", "]]"],
    props: {
        showContactPopup: {
            type: Boolean,
            default: false
        },
        closePopup: Function
    }
})

Vue.component('contact-popup', ContactPopUpComponent)

// new ContactPopUpComponent().$mount('#contactPopUp');
const defaultSliderPriceOptions = {
    type: "double",
    min: 0,
    max: 20,
    from: 0,
    to: 1000,
    step: 0.5,
    grid: true,
    values_separator: "-",
    postfix: "",
    max_postfix: "+",
}
const defaultAreaSliderOptions = {
    type: "double",
    min: 0,
    max: 500,
    from: 0,
    to: 10000,
    step: 0.5,
    grid: true,
    values_separator: "-",
    postfix: "",
    max_postfix: "+",
}

let counter = 0;
const PropertyListComponent = Vue.extend({
    template: '#propertyListTemplate',
    delimiters: ["[[", "]]"],
    props: {
        listings: Array,
        pagination: Object,
        isViewGrid: Boolean,
        isLoading: Boolean,
        showContactProject: Function,
    },
    methods: {
        getListingDetailURL: function (id) {
            return `/listings/${id}`
        },
        getDistrict: function (district_code) {
            return district_code
        }
    },
})

Vue.component('property-list', PropertyListComponent)


new Vue({
    el: "#search-content",
    delimiters: ['[[', ']]'],
    data() {
        return {
            showFilterType: '',
            houseTypes: [
                {type: 'town_house', text: 'Nhà phố'},
                {type: 'shop_house', text: 'Cửa hàng'},
                {type: 'apartment', text: 'Căn hộ'},
                {type: 'land', text: 'Đất nền'},
                {type: 'land_business', text: 'Mặt bằng kinh doanh'},
                {type: 'villa', text: 'Biệt thự'}
            ],
            houseTypeFilter: [],
            tmpHouseTypeFilter: [],
            minPrice: 0,
            maxPrice: 1000,
            minArea: 0,
            maxArea: 20000,
            isViewGrid: true,
            isFirstLoad: true,
            isLoading: false,
            sortOption: 'created',
            showSortOptions: false,
            queryParams: new URLSearchParams(window.location.search),
            listings: [],
            pagination: {},
            scriptsReady: false,
            checkingInterval: null,
            showContactPopup: false,
        }
    },
    computed: {
        filterPriceText: function () {
            if (this.minPrice == 0 && this.maxPrice == 1000) {
                return "Khoảng giá";
            } else if (this.minPrice >= 20) {
                return "Trên 20 tỷ";
            } else {
                return `${this.minPrice} - ${this.maxPrice} tỷ`;
            }
        },
        filterAreaText: function () {
            if (this.minArea == 0 && this.maxArea == 20000) {
                return "Diện tích";
            } else if (this.minArea >= 500) {
                return "Trên 500 m²";
            } else {
                return `${this.minArea}m² - ${this.maxArea}m²`;
            }
        },
        sortString: function () {
            switch (this.sortOption) {
                case 'price_descend':
                    return 'Giá giảm dần';
                case 'price_ascend':
                    return 'Giá tăng dần';
                default:
                    return 'Mới nhất'
            }
        }
    },
    methods: {
        toggleFilterType: function (type) {
            setTimeout(() => {
                if (this.showFilterType != type)
                    this.showFilterType = type;
                else
                    this.showFilterType = '';
            }, 10)

        },
        hideHouseFilters: function () {
            if (this.showFilterType)
                this.showFilterType = '';
        },
        resetHouseFilter: function () {
            this.houseTypeFilter = [];
            $('#leads .check').prop('checked', false);
        },
        cancelHouseFilter: function () {
            this.hideHouseFilters();
            $('#leads .check').prop('checked', false);
            this.houseTypeFilter.map(item => {
                $(`#leads .check[value=${item}]`).prop('checked', true);
            })
        },
        applyHouseFilter: async function () {
            let houseTypeFilter = [];
            $('#leads .check:checked').map((index, item) => {
                if (item.value && this.houseTypes.filter(ht => ht.type === item.value).length > 0) {
                    houseTypeFilter.push(item.value);
                }
            });
            if (JSON.stringify(this.houseTypeFilter) === JSON.stringify(houseTypeFilter)) return;
            this.houseTypeFilter = houseTypeFilter;
            this.updateQueryParams({'housetype': houseTypeFilter.join(',')})
            this.hideHouseFilters();
            await this.getListings();
            this.setMarkers();
        },
        toggleShowSortOptions: function () {
            this.showSortOptions = !this.showSortOptions;
        },
        setPrices: async function (from, to) {
            if (this.minPrice == from && this.maxPrice == to) return;
            this.minPrice = from;
            this.maxPrice = to;
            this.$priceSlider.update({
                ...this.$priceSlider.options,
                from, to
            });
            this.updateQueryParams({minPrice: from, maxPrice: to})
            this.hideHouseFilters();
            await this.getListings();
            this.setMarkers();
        },
        resetPriceSlider: function () {
            this.$priceSlider.update(defaultSliderPriceOptions);
        },
        applySliderPrice: function () {
            const {from, to} = this.$priceSlider.result;
            if (from >= 20) {
                this.setPrices(from, 1000);
            } else {
                this.setPrices(from, to)
            }
        },
        setArea: async function (from, to) {
            if (this.minArea == from && this.maxArea == to) return;
            this.minArea = from;
            this.maxArea = to;
            this.$areaSlider.update({
                ...this.$areaSlider.options,
                from, to
            });
            this.updateQueryParams({minArea: from, maxArea: to})
            this.hideHouseFilters();
            await this.getListings();
            this.setMarkers();
        },
        resetAreaSlider: function () {
            this.$areaSlider.update(defaultAreaSliderOptions);
        },
        applySliderArea: function () {
            const {from, to} = this.$areaSlider.result;
            if (from >= 500) {
                this.setArea(from, 20000);
            } else {
                this.setArea(from, to)
            }
        },
        sortBy: async function (sortOption) {
            if (this.sortOption == sortOption) return;
            this.sortOption = sortOption;
            this.showSortOptions = false;
            this.updateQueryParams({sort: sortOption});
            await this.getListings();
            this.setMarkers();
        },
        viewAsGrid: function () {
            this.isViewGrid = true;
        },
        viewAsList: function () {
            this.isViewGrid = false;
        },
        getQueryParams: function () {
            return this.queryParams;
        },
        updateQueryParams: function (params) {
            const urlParams = this.getQueryParams();
            Object.keys(params).map((key) => {
                if (urlParams.has(key)) {
                    urlParams.set(key, params[key])
                } else {
                    urlParams.append(key, params[key])
                }
            })
            this.queryParams = urlParams;
        },
        removeQueryParams: function (params) {
            const urlParams = this.getQueryParams();
            Object.keys(params).map((key) => {
                if (urlParams.has(key)) {
                    urlParams.delete(key, params[key])
                }
            })
            this.queryParams = urlParams;
        },
        getListings: async function () {
            this.isLoading = true;
            const urlParams = this.getQueryParams();
            try {
                const resp = await axios.get(`/api/search?${urlParams.toString()}`)
                if (resp && resp.status === 200) {
                    const {listings, pagination} = resp.data;
                    this.listings = listings;
                    this.pagination = pagination;
                }
            } catch (e) {
                this.listings = [];
                this.pagination = {};
            }

            this.isLoading = false;
        },
        goTo: async function (page) {
            this.updateQueryParams({page})
            await this.getListings();
            this.setMarkers();
        },
        applySearchParams: async function () {

        },
        showContactProject: function () {
            this.showContactPopup = true;
        },
        closeContactProject: function () {
            this.showContactPopup = false;
        },
        setMarkers: function () {
            if (!map) return;
            this.listings.map(item => {
                markers.push(
                    new google.maps.Marker({
                        position: new google.maps.LatLng(item.lat, item.long),
                        title: item.title,
                        map: map,
                        icon: normalIcon(),
                    })
                );
            })
        },
        initMap: function () {
            if (!google) return;
            const mapOptions = {
                zoom: 15,
                center: new google.maps.LatLng(21.0334474, 105.8401439),  // Hanoi
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            map = new google.maps.Map(document.getElementById('search-map'), mapOptions);
        },
        clearMarkers: function () {
            for (let i = 0; i < markers.length; i++) {
                markers[i].setMap(null)
            }
            markers = [];
        },
        checkIntervalCallback: function () {
            if (axios) {
                this.scriptsReady = true;
            }
            counter++;
            if (counter >= 20) {
                clearInterval(this.checkingInterval);
            } else {
                clearInterval(this.checkingInterval);
                const timeout = 200 + counter * 40;
                this.checkingInterval = setInterval(this.checkIntervalCallback, timeout);
            }
        }
    },
    created() {
        this.checkingInterval = setInterval(this.checkIntervalCallback, 200);
        window.initMap = this.initMap;
    },
    mounted() {
        setTimeout(() => {
            $(this.$refs.priceInput).ionRangeSlider({
                ...defaultSliderPriceOptions,
            });
            this.$priceSlider = $(this.$refs.priceInput).data('ionRangeSlider');

            $(this.$refs.areaInput).ionRangeSlider({
                ...defaultAreaSliderOptions,
            });
            this.$areaSlider = $(this.$refs.areaInput).data('ionRangeSlider');
        }, 100);
    },
    watch: {
        scriptsReady: async function () {
            clearInterval(this.checkingInterval);
            await this.getListings();
            this.setMarkers();
        }
    },
    destroyed: function () {
        this.$priceSlider.destroy()
    }
})

