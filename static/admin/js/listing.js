var ChuSo = [" không ", " một ", " hai ", " ba ", " bốn ", " năm ", " sáu ", " bảy ", " tám ", " chín "];
var Tien = ["", " nghìn", " triệu", " tỷ", " nghìn tỷ", " triệu tỷ"];
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
    var ViTri = [];
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

    function updateWard() {
        const selector = $(`#${wardId}`);
        const curVal = selector.val() || "";
        if (curVal) {
            selector.replaceWith(`<select name="ward" id="id_ward"><option selected value="${curVal}">${curVal}</option></select>`);
        } else {
            selector.replaceWith('<select name="ward" id="id_ward"></select>');
        }
        updateSelectOptions(wardChannel, $(`#${districtId}`).val() || '008', `#${wardId}`, "Chọn Phường/xã")
    }

    function updateSelectOptions(channel, code, selector, defaultText) {
        $.ajax(buildURL(channel, code)).done((result) => {
            if (Array.isArray(result)) {
                // let optionText = [`<option value="" disabled selected>${defaultText}</option>`]
                let optionText = []
                const curVal = $(selector).val();
                result.map(item => {
                    if (item.value == curVal) {
                        optionText.push(`<option selected value="${item.value}">${item.repr}</option>`)
                    } else {
                        optionText.push(`<option value="${item.value}">${item.repr}</option>`)
                    }
                });
                $(selector).html(optionText);
            }
        })
    }

    function updateSelect(parentId, childId, channel, defaultText) {
        $(`#${parentId}`).change((e) => {
            const parentCode = e.target.value;
            if (!parentCode) return;
            updateSelectOptions(channel, parentCode, `#${childId}`, defaultText);
        })
    }

    updateSelect(stateId, districtId, districtChannel, "Chọn quận/huyện truoc")
    updateSelect(districtId, wardId, wardChannel, "Chọn Phường/xã")
    updateWard();
    const address$ = $('#id_address');

    $('#id_street').typingFinished(500, (e) => {
        const street = e.target.value
        const state = $('#id_state option:selected').text()
        const district = $('#id_district option:selected').text()
        if (state && district && street && !address$.val()) {
            address$.val(`${street}, ${district}, ${state}`)
            address$.trigger('keyup')
        }
    })
}

function multipleImages($) {
    // Delete link available  -> is editing listing
    const isEdit = $('p.deletelink-box .deletelink').length > 0;
    const selector$ = $('#listingimage_set-group .module');
    let deleteBoxes$ = {};
    const existingImages = $('.has_original.dynamic-listingimage_set').map(function (i, el) {
        const el$ = $(el)
        const imgId = el$.find('.original [id$="-id"]').val();
        deleteBoxes$[imgId] = el$.find(`#id_${el$.attr('id')}-DELETE`).first();
        const url = el$.find('.field-photo a').attr('href');
        const name = url.split('/').pop();
        // return url;
        return {
            source: url,
            options: {
                metadata: {
                    id: imgId,
                    name: name
                }
            }
        }
    }).get();
    FilePond.registerPlugin(
        FilePondPluginImagePreview,
        FilePondPluginImageExifOrientation,
        FilePondPluginFileValidateSize,
        FilePondPluginFileValidateType
    );

    MicroModal.init({})

    const nameAttr = 'listingimage_set';

    // FilePond.create(document.querySelector('.filepond'));
    const pond = FilePond.create({
        allowMultiple: true,
        name: nameAttr,
        labelIdle: "<span class=\"filepond--label-action\">Nhấp để chọn hoặc kéo ảnh vào đây</span>",
        acceptedFileTypes: ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'],
        files: existingImages,
        maxFiles: 20,
        maxFileSize: '5MB',
        // beforeRemoveFile: async function (item) {
        //     const imgId = item.getMetadata('id');
        //     if (imgId) {
        //         MicroModal.show('warning-modal');
        //         return new Promise(function (resolve) {
        //             setTimeout(resolve.bind(null, true), 3000)
        //         });
        //     }
        // }
    });
    const fixNameAttr = (el$, name) => {
        el$.attr('name', name)
    }
    pond.on('addfile', function (error, file) {
        // Add saved tag to existing pics
        if (file.file.constructor.name === 'Blob') {
            $(`#filepond--item-${file.id} .filepond--file-info-main`).append(' (Đã lưu)')
        }
        fixNameAttr(selector$.find('input.filepond--browser'), nameAttr);

        const lst = new DataTransfer();
        pond.getFiles().map(item => {
            const fileType = item.file.constructor.name;
            if (fileType === 'File') {
                lst.items.add(item.file)
            }
        })
        selector$.find("input.filepond--browser").prop("files", lst.files);
    });

    pond.on('removefile', (error, file) => {
        const imgId = file.getMetadata('id');
        deleteBoxes$[imgId].attr('checked', true);
        fixNameAttr(selector$.find('input.filepond--browser'), nameAttr);
    });

    if (isEdit) {
        selector$.find('table').first().hide();
    }

    // selector$.html(
    //     '<h2>Listing images</h2>'
    // );
    selector$.append(pond.element);

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function importToDB($) {
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

    myDropzone.on("success", function (file, response) {
        this.removeFile(file);
        $('.modal-alert').removeClass().text('Tải lên thành công!').addClass('alert alert-success')
    });

    $('#sendImportFile').on('click', () => {
        myDropzone.processQueue();
    })
}


function importListing($) {
    $('body').append('<!-- Modal -->\n' +
        '<div class="modal fade" id="importListingModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">\n' +
        '  <div class="modal-dialog" role="document">\n' +
        '    <div class="modal-content">\n' +
        '      <div class="modal-header">\n' +
        '        <h5 class="modal-title" id="exampleModalLabel">Nhập dữ liệu BĐS từ file .csv</h5>\n' +
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
   $('.object-tools').append('<li><button onclick="importToDB($)" class="button" type="button" data-toggle="modal" data-target="#importListingModal">Nhập dữ liệu từ file Excel</button></li>');
}

function exportFBData($) {
    const csrftoken = getCookie('csrftoken');

    function downloadURI(uri, name) {
        let link = document.createElement("a");
        link.download = name;
        link.href = uri;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    $.ajax('/api/download_fb_export', {
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
    }).done((data, status, xhr) => {
        if (status === 'success') {
            const fileName = xhr.getResponseHeader('Content-Disposition').split('=').pop()
            downloadURI(`data:text/csv,${data}`, fileName)
        }
    }).fail(err => {
        console.log(err);
    })

}

function exportListing($) {
    $('.object-tools').append('<li><button class="button" onclick="exportFBData($)" type="button">Xuất dữ liệu csv (Facebook)</button></li>');
}

window.addEventListener("load", function () {
    (function (jQuery) {
        // priceToText(jQuery);
        addressSelect(jQuery);
        importListing(jQuery);
        multipleImages(jQuery)
        exportListing(jQuery);
    })(django.jQuery);
});
