$(function () {

    var setDonorForm = function () {

        var email       = document.getElementById('id_email');
        var telephone   = document.getElementById('id_telephone_number');
        var mobile      = document.getElementById('id_mobile_number');
        var ref         = document.getElementById('id_customer_ref');
        var needReceipt = document.getElementById('id_want_receipt');
        var address     = document.getElementById('id_address_line');
        var city        = document.getElementById('id_city');
        var province    = document.getElementById('id_province');
        var postalCode  = document.getElementById('id_postal_code');

        return function (data) {
            email.value         = data.email;
            telephone.value     = data.telephone_number;
            mobile.value        = data.mobile_number;
            ref.value           = data.customer_ref;
            needReceipt.value   = data.want_receipt;
            address.value       = data.address_line;
            city.value          = data.city;
            province.value      = data.province;
            postalCode.value    = data.postal_code;

            printDonationList(data.donation_records);
        };
    }();

    var setItemForm = function() {

        var header = document.getElementById('item_header');

        return function (e, data) {
            if (!e) {
                header.innerText = "Item";
            }
        }
    };

    var setDonationForm = function() {
        var donorName       = document.getElementById('id_donor_name');

        var donationForm    = document.getElementById('donation_form');

        var deleteButton    = document.getElementById('btn_delete_donation');
        var saveButton      = document.getElementById('btn_save_donation');
        var updateButton    = document.getElementById('btn_update_donation');
        var addNewButton    = document.getElementById('btn_add_new_donation');
        var cancelButton    = document.getElementById('btn_cancel_donation');

        var taxReceiptNoDiv = document.getElementById('donation_form').getElementsByClassName('field-tax_receipt_no')[0];

        var taxReceiptField             = document.getElementById('id_tax_receipt_no');
        var donationDateField           = document.getElementById('id_donate_date');
        var donationVerifiedCheckBox    = document.getElementById('id_verified');
        var donationPickUpField         = document.getElementById('id_pick_up');

        var header = document.getElementById('donation_header');

        return function (e, data) {

            if (donorName.value == '') {
                alert("Enter donor info first");
                scrollTo(donorName);
                return;
            }

            // [1] event when form closed
            if (this == cancelButton || !e) {
                donationForm.hidden = true;
                addNewButton.hidden = false;
                saveButton.hidden   = true;
                cancelButton.hidden = true;
                deleteButton.hidden = true;
                updateButton.hidden = true;
                header.hidden = true;

                taxReceiptField.value   = '';
                donationDateField.value = '';
                donationVerifiedCheckBox.checked = false;
                donationPickUpField.value = '';

                printItemList(null);
                return;
            }

            // [2] even when opening form
            if (this == addNewButton) {

                deleteButton.hidden     = true;
                saveButton.hidden       = false;
                updateButton.hidden     = true;

                taxReceiptNoDiv.hidden  = true;

                header.hidden = false;
                header.innerText = "New Donation";

                printItemList(null);
                scrollTo('#donation_form');
            }
            // [3] even when setting form
            else {

                deleteButton.hidden     = false;
                saveButton.hidden       = true;
                updateButton.hidden     = false;

                // taxReceiptNoDiv.hidden  = false;

                header.hidden = false;
                header.innerText = data.tax_receipt_no;

                taxReceiptField.value               = data.tax_receipt_no;
                donationDateField.value             = data.donate_date;
                donationVerifiedCheckBox.checked    = (data.verified == 'true');
                donationPickUpField.value           = data.pick_up;
            }

        donationForm.hidden = false;
        addNewButton.hidden = true;
        cancelButton.hidden = false;
    };
    }();

    $("#id_donor_name").autocomplete({
        source: getNames.bind(this),
        minLength: 1,
        select: requestDonorInfo
    });

    /**
     * request list of names for autocomplete
     *
     * minLength : minimum length required to execute ajax
     * { key : <string> }
     *  response data = [ <name1>, <name2>]
     */
    function getNames (request, response) {
        $.ajax({
            url: "/add/autocomplete_name",
            dataType: "json",
            data: {
                key: this.value
            },
            success: function (data) {
                response(data.result);
            },
            error: function () {
                console.error(arguments);
            }
        });
    }

    /**
     * request donor information & donation records
     *
     * request : { donor_name : <donor_name> }
     * response : { email : <donor_email>,
     *              telephone_numb : <telephone>,
     *              mobile_number : <mobile>,
     *              customer_ref : <customer>,
     *              want_receipt : <whether receipt requested>,
     *              address_line : <address>,
     *              city : <city>,
     *              province : <province>,
     *              postal_code : <postal_code>
     *              donation_records : [ {
     *                      tax_receipt_no : <tax_receipt_no>,
     *                      donate_date : <donation_date>,
     *                      pick_up : <pick_up location>
     *              }, ... ]
     *     }
     */
    function requestDonorInfo(e, ui) {
        $.ajax({
                url: "/add/get_donor_data",
                dataType: "json",
                data: {
                    donor_name: ui.item.value
                },
                success: setDonorForm,
                error: function () {
                    console.error(arguments);
                }
        });
    }

    /**
     * print donation list
     * data = [ { tax_receipt_no : <tax_receipt_no>,
     *            donate_date : <donation_date>,
     *            pick_up : <pick_up location>
     *          }, ... ]
     */
    var printDonationList = function () {

        var donation_result_div = document.getElementById('donation_result_list');
        var donation_table_body = donation_result_div.getElementsByTagName("tbody")[0];

        return function (data) {
            var html = '';
            var donation;
            for (var ix = 0, ixLen = data.length; ix < ixLen; ix++) {
                donation = data[ix];
                html += '<tr class="row' + ((ix % 2) ? 2 : 1) + '" id="' + donation.tax_receipt_no + '" >\n' +
                    '    <td class="field-tax_receipt_no">' + donation.tax_receipt_no + '</td>\n' +
                    '    <td class="field-donate_date nowrap">' + donation.donate_date + '</td>\n' +
                    '    <td class="field-pick_up">' + donation.pick_up + '</td>\n' +
                    '    <td class="field-verified">' +
                    ((donation.verified) ? '<img src="/static/admin/img/icon-yes.svg" alt=true>' : '<img src="/static/admin/img/icon-no.svg" alt=false>') +
                    '    </td>\n' +
                    '</tr>';
            }

            setDonationForm.call(this, null);
            scrollTo(donation_result_div);
            donation_table_body.innerHTML = html;
        };
    }();

    var printItemList = function () {

        var item_result_div = document.getElementById('item');
        var item_table_body = item_result_div.getElementsByTagName('tbody')[0];
        var header = document.getElementById('item_header');

        return function (data) {

            if (!data) {
                item_result_div.hidden = true;
                setItemForm(null);
                return;
            }

            item_result_div.hidden = false;
            header = this.id;

            var html = '';
            var item;
            for (var ix = 0, ixLen = data.length; ix < ixLen; ix++) {
                item = data[ix];
                html += '<tr class="row' + ((ix % 2) ? 2 : 1) + '" id="' + item.item_id + '" >\n' +
                    // '                        <td class="action-checkbox"><input type="checkbox" name="_selected_action" value='+item.item_id +'\n' +
                    // '                                                           class="action-select"></td>\n' +
                    '<th class="field-get_item">'+item.item_id+'</th>\n' +
                    '<td class="field-manufacturer">'+item.manufacturer+'</td>\n' +
                    '<td class="field-model">'+item.model+'</td>\n' +
                    '<td class="field-quantity">'+item.quantity+'</td>\n' +
                    '<td class="field-batch">'+item.batch+'</td>\n' +
                    '<td class="field-verified">' +
                    ((item.verified) ? '<img src="/static/admin/img/icon-yes.svg" alt=true>' : '<img src="/static/admin/img/icon-no.svg" alt=false>') +
                    '</td>\n' +
                    '</tr>';
            }

            setItemForm.call(this, null);
            // scrollTo(item_result_div);
            item_table_body.innerHTML = html;
        };
    }();

    $("#donation_result_list").delegate("tr", "click", function (e) {
        if (this.children[0].nodeName == 'TH') return;

        var tr = this.children;
        var data = {};

        data.tax_receipt_no = tr[0].innerText;
        data.donate_date    = tr[1].innerText;
        data.pick_up        = tr[2].innerText;
        data.verified       = tr[3].getElementsByTagName("img")[0].alt;

        setDonationForm(e, data);
        getItems.call(this, data.tax_receipt_no);
        scrollTo(this);
    });


    $("#item_result_list").delegate("tr", "click", function (e) {
        if (this.children[0].nodeName == 'TH') return;

        var tr = this.children;
        var data = {};

        setItemForm(e, data);
        scrollTo(this);
    });

    var getItems = function () {
        g = this;
        $.ajax({
            url: "/add/get_items",
            dataType: "json",
            data: {
                tax_receipt_no: this.id
            },
            success: printItemList.bind(g),
            error: function () {
                console.error(arguments);
            }
        });
    };

    var saveDonation = function () {
        var form = $(document.getElementById('donation_form').getElementsByTagName('form')[0]);

        return function () {
            $.ajax({
                url: "/add/save_donation_data",
                dataType: "json",
                data: form.serialize(),
                success: printDonationList,
                error: function () {
                    console.error(arguments);
                }
            });
        };
    }();

    $('#btn_add_new_donation').on('click', setDonationForm);
    $('#btn_cancel_donation').on('click', setDonationForm);
    $('#btn_save_donation').on('click', saveDonation);

    function scrollTo(id) {
          $('html, body').animate({
            scrollTop: $(id).offset().top + 'px'
        }, 'fast');

          console.log(id.nodeName);
          if (id.nodeName == "INPUT") {
              $(id).focus();
          }
    }
});