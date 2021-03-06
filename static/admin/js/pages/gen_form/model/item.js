"use strict";
define(["../util/util"], function(util) {
    class Item {
        constructor(data = {}) {
            this.taxReceiptNo = data.taxReceiptNo;
            this.id = data.id;
            this.description = data.description;
            this.particulars = data.particulars;
            this.manufacturer = data.manufacturer;
            this.model = data.model;
            this.quantity = data.quantity;
            this.working = data.working;
            this.condition = data.condition;
            this.quality = data.quality;
            this.batch = data.batch;
            this.value = data.value;
            this.verified = data.verified;
            this.status = data.status;
        }

        toJson() {
            return {
                taxReceiptNo: this.taxReceiptNo,
                id: this.id,
                description: this.description,
                particulars: this.particulars,
                manufacturer: this.manufacturer,
                model: this.model,
                quantity: this.quantity,
                working: this.working,
                condition: this.condition,
                quality: this.quality,
                batch: this.batch,
                value: this.value,
                status: this.status,
                verified: this.verified
            };
        }

        /**
         * Takes a success callback and id and get related item
         * @param {ID} id
         * @param {Function} successFn
         */
        get(id, successFn = util.noop) {
            return util.ajax({
                url: "/api/item",
                type: "GET",
                data: {
                    id: id
                },
                success: successFn,
            });
        }

        /**
         * Takes a success callback and saves the current item
         * @param {Function} successFn
         */
        save(successFn = util.noop) {
            return util.ajax({
                url: "/api/item",
                type: "POST",
                data: this.toJson(),
                success: successFn,
            });
        }
        /**
         * Takes a success callback and updates the current item
         * @param {Function} successFn
         */
        update(successFn = util.noop) {
            return util.ajax({
                url: "/api/item",
                type: "PUT",
                data: this.toJson(),
                success: successFn,
            });
        }

        /**
         * Takes a success callback and updates the current item
         * @param {Function} successFn
         */
        delete(successFn = util.noop) {
            return util.ajax({
                url: "/api/item",
                type: "DELETE",
                data: {
                    id: this.id
                },
                success: successFn,
            });
        }
    }


    /**
     * Take a success callback and get related items based on taxReceiptNo
     * @param {ID} taxReceiptNo
     * @param {Function} successFn
     */
    Item.getRelated = function(taxReceiptNo, successFn = util.noop) {
        return util.ajax({
            url: "/api/related_items",
            type: "GET",
            data: {
                taxReceiptNo: taxReceiptNo
            },
            success: successFn,
        });
    };

    return Item;
});
