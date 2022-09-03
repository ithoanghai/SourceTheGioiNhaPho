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
    // const fileUploader = $('#fileUpload').dropzone({url: 'import-export', autoProcessQueue: false});
    var myDropzone = new Dropzone("#fileUpload", {
        url: "import-export",
        autoProcessQueue: false,
        maxFilesize: 20,    // MB
        createImageThumbnails: false,
        maxFiles: 10,
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

function exportRealtorData($) {
    const csrftoken = getCookie('csrftoken');

    function downloadURI(uri, name) {
        let link = document.createElement("a");
        link.download = name;
        link.href = uri;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    $.ajax('/api/download_export_realtor', {
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


function importRealtor($) {
    $('body').append('<!-- Modal -->\n' +
        '<div class="modal fade" id="importRealtorModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">\n' +
        '  <div class="modal-dialog" role="document">\n' +
        '    <div class="modal-content">\n' +
        '      <div class="modal-header">\n' +
        '        <h5 class="modal-title" id="exampleModalLabel">Nhập dữ liệu Chuyên viên từ file Excel</h5>\n' +
        '        <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n' +
        '          <span aria-hidden="true">&times;</span>\n' +
        '        </button>\n' +
        '      </div>\n' +
        '      <div class="modal-body">\n' +
        '        <form action="import-export"\n' +
        '              class="dropzone"\n' +
        '              id="fileUpload">' +
        '         </form>' +
        '      <p style="margin-top: 1em" class="modal-alert"></p>\n' +
        '      </div>\n' +
        '      <div class="modal-footer">\n' +
        '        <button type="button" class="btn btn-secondary" data-dismiss="modal">Hủy</button>\n' +
        '        <button type="button" id="sendImportFile" class="btn btn-primary">Nhập liệu</button>\n' +
        '      </div>\n' +
        '    </div>\n' +
        '  </div>\n' +
        '</div>')
    $('.extrabutton').append('<li><button onclick="importToDB($)" class="button" type="button" data-toggle="modal" data-target="#importRealtorModal">Nhập dữ liệu Chuyên viên từ file Excel</button></li>');
}

function exportRealtor($) {
    $('.extrabutton').append('<li><button class="button" onclick="exportRealtorData($)" type="button">Xuất dữ liệu Chuyên viên ra Excel</button></li>');
}

window.addEventListener("load", function () {
    (function (jQuery) {
        $.ajax('/api/current_user', {
            type: 'GET'
        }).done((data, status) => {
            if (data.can_import_realtor) {
                importRealtor(jQuery);
            }
            if (data.can_export_realtor) {
                exportRealtor(jQuery);
            }
        })
        // priceToText(jQuery);
        addressSelect(jQuery);
        multipleImages(jQuery)
    })(django.jQuery);
});
