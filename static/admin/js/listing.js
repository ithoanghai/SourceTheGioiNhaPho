var ChuSo = new Array(" không ", " một ", " hai ", " ba ", " bốn ", " năm ", " sáu ", " bảy ", " tám ", " chín ");
var Tien = new Array("", " nghìn", " triệu", " tỷ", " nghìn tỷ", " triệu tỷ");
const URL = '/cadastral/ajax_lookup';
const districtChannel = 'districts';
const wardChannel = 'wards';
const stateId = 'id_state';
const districtId = 'id_district';
const wardId = 'id_ward';

function buildURL(channel, term) {
    return `${URL}/${channel}?term=${term}`
}

function DocSo3ChuSo(baso) {
    var tram;
    var chuc;
    var donvi;
    var KetQua = "";
    tram = parseInt(baso / 100);
    chuc = parseInt((baso % 100) / 10);
    donvi = baso % 10;
    if (tram == 0 && chuc == 0 && donvi == 0) return "";
    if (tram != 0) {
        KetQua += ChuSo[tram] + " trăm ";
        if ((chuc == 0) && (donvi != 0)) KetQua += " linh ";
    }
    if ((chuc != 0) && (chuc != 1)) {
        KetQua += ChuSo[chuc] + " mươi";
        if ((chuc == 0) && (donvi != 0)) KetQua = KetQua + " linh ";
    }
    if (chuc == 1) KetQua += " mười ";
    switch (donvi) {
        case 1:
            if ((chuc != 0) && (chuc != 1)) {
                KetQua += " mốt ";
            } else {
                KetQua += ChuSo[donvi];
            }
            break;
        case 5:
            if (chuc == 0) {
                KetQua += ChuSo[donvi];
            } else {
                KetQua += " lăm ";
            }
            break;
        default:
            if (donvi != 0) {
                KetQua += ChuSo[donvi];
            }
            break;
    }
    return KetQua;
}

function DocTienBangChu(SoTien) {
    var lan = 0;
    var i = 0;
    var so = 0;
    var KetQua = "";
    var tmp = "";
    var ViTri = new Array();
    if (SoTien < 0) return "Số tiền âm !";
    if (SoTien == 0) return "Không đồng !";
    if (SoTien > 0) {
        so = SoTien;
    } else {
        so = -SoTien;
    }
    if (SoTien > 8999999999999999) {
        //SoTien = 0;
        return "Số quá lớn!";
    }
    ViTri[5] = Math.floor(so / 1000000000000000);
    if (isNaN(ViTri[5]))
        ViTri[5] = "0";
    so = so - parseFloat(ViTri[5].toString()) * 1000000000000000;
    ViTri[4] = Math.floor(so / 1000000000000);
    if (isNaN(ViTri[4]))
        ViTri[4] = "0";
    so = so - parseFloat(ViTri[4].toString()) * 1000000000000;
    ViTri[3] = Math.floor(so / 1000000000);
    if (isNaN(ViTri[3]))
        ViTri[3] = "0";
    so = so - parseFloat(ViTri[3].toString()) * 1000000000;
    ViTri[2] = parseInt(so / 1000000);
    if (isNaN(ViTri[2]))
        ViTri[2] = "0";
    ViTri[1] = parseInt((so % 1000000) / 1000);
    if (isNaN(ViTri[1]))
        ViTri[1] = "0";
    ViTri[0] = parseInt(so % 1000);
    if (isNaN(ViTri[0]))
        ViTri[0] = "0";
    if (ViTri[5] > 0) {
        lan = 5;
    } else if (ViTri[4] > 0) {
        lan = 4;
    } else if (ViTri[3] > 0) {
        lan = 3;
    } else if (ViTri[2] > 0) {
        lan = 2;
    } else if (ViTri[1] > 0) {
        lan = 1;
    } else {
        lan = 0;
    }
    for (i = lan; i >= 0; i--) {
        tmp = DocSo3ChuSo(ViTri[i]);
        KetQua += tmp;
        if (ViTri[i] > 0) KetQua += Tien[i];
        if ((i > 0) && (tmp.length > 0)) KetQua += ',';//&& (!string.IsNullOrEmpty(tmp))
    }
    if (KetQua.substring(KetQua.length - 1) == ',') {
        KetQua = KetQua.substring(0, KetQua.length - 1);
    }
    KetQua = KetQua.substring(1, 2).toUpperCase() + KetQua.substring(2);
    return KetQua;//.substring(0, 1);//.toUpperCase();// + KetQua.substring(1);
}

function priceToText($) {
    $('<span id="id_price_text"></span>').appendTo('.form-row.field-price > div');
    const price = $('#id_price').val();
    if (price) {
        $('#id_price_text').text(DocTienBangChu(price));
    }
    $('#id_price').change((event) => {
        $('#id_price_text').text(DocTienBangChu(event.target.value));
    });
}

function addressSelect($) {
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
}

function importListing($) {
    $('body').append('<!-- Modal -->\n' +
        '<div class="modal fade" id="importListingModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">\n' +
        '  <div class="modal-dialog" role="document">\n' +
        '    <div class="modal-content">\n' +
        '      <div class="modal-header">\n' +
        '        <h5 class="modal-title" id="exampleModalLabel">Nhập dữ liệu nhà phố từ file</h5>\n' +
        '        <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n' +
        '          <span aria-hidden="true">&times;</span>\n' +
        '        </button>\n' +
        '      </div>\n' +
        '      <div class="modal-body">\n' +
        '        <form action="import-listing"\n' +
        '              class="dropzone"\n' +
        '              id="fileUpload">' +
        '         </form>' +
        '      <p style="margin-top: 1em" class="modal-alert"></p>\n' +
        '      </div>\n' +
        '      <div class="modal-footer">\n' +
        '        <button type="button" class="btn btn-secondary" data-dismiss="modal">Hủy</button>\n' +
        '        <button type="button" id="sendImportFile" class="btn btn-primary">Gửi lên</button>\n' +
        '      </div>\n' +
        '    </div>\n' +
        '  </div>\n' +
        '</div>')
    $('.object-tools').append('<li><button type="button" class="addlink" data-toggle="modal" data-target="#importListingModal">Nhập từ Excel</button></li>')
    const csrfCookie = document.cookie.split('; ').find(item => item.startsWith('csrftoken=')).split('=')
    let csrf = ''
    try {
        csrf = csrfCookie[1];
    } catch (e) {
    }
    // const fileUploader = $('#fileUpload').dropzone({url: 'import-listing', autoProcessQueue: false});
    var myDropzone = new Dropzone("#fileUpload", {
        url: "import-listing",
        autoProcessQueue: false,
        maxFilesize: 10,    // MB
        createImageThumbnails: false,
        maxFiles: 1,
        acceptedFiles: 'text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });
    myDropzone.on('sending', (file, xhr, formData) => {
        formData.append('csrfmiddlewaretoken', csrf)
    })

    // myDropzone.on('addedfile', (file) => {
    //     console.log(file)
    // })

    myDropzone.on("success", function (file, response) {
        this.removeFile(file);
        $('.modal-alert').removeClass().text('Tải lên thành công!').addClass('alert alert-success')
    });

    $('#sendImportFile').on('click', () => {
        myDropzone.processQueue();
    })
}

window.addEventListener("load", function () {
    // (function (jQuery) {
    //     priceToText(jQuery);
    //     addressSelect(jQuery);
    //     importListing(jQuery);
    // })(django.jQuery);
});
