const URL = '/cadastral/ajax_lookup';
const districtChannel = 'districts';
const wardChannel = 'wards';
const stateId = 'id_state';
const districtId = 'id_district';
const wardId = 'id_ward';

function buildURL(channel, term) {
    return `${URL}/${channel}?term=${term}`
}


window.addEventListener("load", function () {

    (function ($) {
        $.fn.typingFinished = function (timeout, callback) {
            let timer = undefined,
                self = $(this);

            self.keyup(function (e) {
                if (typeof timer == "undefined") {
                    timer = setTimeout(function () {
                        callback(e);
                    }, timeout);
                }
            }).keydown(function () {
                if (typeof timer !== "undefined") {
                    clearTimeout(timer);
                    timer = undefined;
                }
            });

            return self;
        }

        function updateSelect(parentId, childId, channel, text) {
            $(`#${parentId}`).change((e) => {
                const parentCode = e.target.value;
                if (!parentCode) return;
                $.ajax(buildURL(channel, parentCode)).done((result) => {
                    if (Array.isArray(result)) {
                        let optionText = [`<option value=\"\" selected=\"\">${text}</option>`]
                        result.map(item => {
                            optionText.push(item.repr)
                        });
                        $(`#${childId}`).html(optionText);
                    }
                })
            })
        }

        updateSelect(stateId, districtId, districtChannel, "Chọn quận/huyện")
        updateSelect(districtId, wardId, wardChannel, "Chọn Phường/xã")
        const address$ = $('#id_address');

        $('#id_street').typingFinished(500, (e) => {
            const street = e.target.value
            const state = $('#id_state option:selected').text()
            const district = $('#id_district option:selected').text()
            if (state && district && street) {
                address$.val(`${street}, ${district}, ${state}`)
                address$.trigger('keyup')
            }
        })
    })(django.jQuery);
});