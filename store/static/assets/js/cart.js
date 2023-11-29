$(document).on('click', '#addtoCartBtn',
    function() {
        $("#addtoCartBtn").on('click', function() {
            var _vm = $(this);
            var _btnqty = $("#number").val();
            var _btnId = $(".proID").val();
            var _btnname = $(".proname").val();
            var _btnprice = $(".product-price").text();
            var _btnimg = $(".pronimg").val();

            console.log(_btnqty, _btnname, _btnId, _btnprice, _btnimg);
            // them sap pham 
            $.ajax({
                url: '/add-to-cart/',
                data: {
                    'id': _btnId,
                    'qty': _btnqty,
                    'name': _btnname,
                    'image': _btnimg,
                    'price': _btnprice
                },
                dataType: 'json',
                beforeSend: function() {
                    _vm.attr('disabled', true);
                },
                success: function(res) {
                    $(".cart-list").text(res.totalitems);
                    _vm.attr('disabled', false);
                    location.reload();
                }

            });
            //end



        })
    })



$(document).on('click', '.delete-item', function() {
        var _btndel = $(this).attr('data-item')
        var _vm = $(this);
        console.log(_btndel)

        // Ajax
        $.ajax({
            url: '/delete-from-cart/',
            data: {
                'id': _btndel,
            },
            dataType: 'json',
            beforeSend: function() {
                _vm.attr('disabled', true);
            },
            success: function(res) {
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled', false);
                $("#cartList").html(res.data);
                location.reload();
            }
        });

        // End
    })
    // delete cart 


// Update item from cart
$(document).on('click', '.update-item', function() {
    var _pId = $(this).attr('data-item');
    var _pQty = $(".product-qty-" + _pId).val();
    var _vm = $(this);
    // Ajax
    $.ajax({
        url: '/update-cart/',
        data: {
            'id': _pId,
            'qty': _pQty
        },
        dataType: 'json',
        beforeSend: function() {
            _vm.attr('disabled', true);
        },
        success: function(res) {
            // $(".cart-list").text(res.totalitems);
            _vm.attr('disabled', false);
            $("#cartList").html(res.data);
            location.reload()
        }
    });;
    // End
});