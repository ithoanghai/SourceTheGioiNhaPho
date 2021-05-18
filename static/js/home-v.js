new Vue({
    delimiters: ['${', '}$'],
    el: '#app',
    data: {
        listings: []

    },
    http: {
        root: 'http://localhost:8888',
        headers: {
            Authorization: 'Token a322f813185fe6d757db3500171fbaa945d72430'
          }
    },
    methods: {
        getListings: function () {
            // this.$http.get('listings/listingsAPI1/').then(function (data,status,request) {
            // if (status == 200) {
            //     this.listings = data.body.results;
            //  }
            // })
        }
    },
    mounted: function () {
        this.getListings();
    }
})