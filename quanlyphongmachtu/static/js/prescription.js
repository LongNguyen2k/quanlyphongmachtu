function addToPrescription(id, name, unitmedicine_name, usage, unitprice){
    event.preventDefault()
    // trả ra đối tượng promise
    fetch('/api/add-to-prescription', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'unitmedicine_name': unitmedicine_name,
             'usage': usage,
            'unitprice': unitprice
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)

        let counter = document.getElementsByClassName('prescriptionCounter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
    }).catch(function(err) {
        console.error(err)
    })


}

function addPrescription(userinfo_id, thongtinbenhnhan_id, total_amount) {
    if(confirm('Khi Chọn Kê Đơn Sẽ Ghi Nhận Đơn Thuốc Cho Bệnh Nhân Đăng Ký Khám! Tiếp Tục?') == true) {
        let trieuchung = document.getElementById('idTrieuChung')
        let dudoanbenh = document.getElementById('idDuDoanLoaiBenh')
        let cachdungthuoc = document.getElementById('idcachdung_thuoc')
            if ( (trieuchung.value === "") || (dudoanbenh.value === "") || (cachdungthuoc.value === "")) {
                alert("Vui Lòng nhập thông tin cho phiếu khám")
            }
            else
            {
                fetch('/api/add-prescription', {
                    method: 'post',
                    body: JSON.stringify({
                        'trieuchung': trieuchung.value,
                        'dudoanbenh': dudoanbenh.value,
                        'user_dangkykham': userinfo_id,
                        'phieukhambenh': thongtinbenhnhan_id,
                        'cachdungthuoc': cachdungthuoc.value,
                        'total_amount': total_amount
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(function(res) {
                    return res.json()
                }).then(function(data){
                    if(data.code == 200)
                        window.location.replace("/bacsi/thanhtoan/"+thongtinbenhnhan_id)
                    else if( data.code == 400)
                            alert(data.err_msg)

                }).catch(err => console.error(err))

            }
    }

}

// hàm này và hàm thêm trong .then res.json là như nhau chỉ là viết gọn hơn
function updatePrescription(id, obj) {
    fetch('/api/update-to-prescription', {
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)

        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {

        let counter = document.getElementsByClassName('prescriptionCounter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
        let amount = document.getElementById('total_amount')
        amount.innerText = new Intl.NumberFormat().format(data.total_price)

    }).catch(function(err){
        console.error(err)
    })
}

function deletePrescription(id){
    if( confirm("Bác Sĩ Có Đồng Ý Xóa Thuốc Này Khỏi Toa Thuốc Không?") == true){
            fetch('/api/delete-to-prescription/' + id, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {

            let counter = document.getElementsByClassName('prescriptionCounter')
            for (let i = 0; i < counter.length; i++)
                counter[i].innerText = data.total_quantity
            let amount = document.getElementById('total_amount')
            amount.innerText = new Intl.NumberFormat().format(data.total_price)
            let element_medicine = document.getElementById('medicine' + id)
            element_medicine.style.display = "none"

           }).catch(function(err){
            console.error(err)
        })
    }
}


function pay_receipt(idphieukham, id_tienkham, tongtien_hoadon){
    if( confirm("Bác Sĩ Đồng Ý Thanh Toán Hóa Đơn! Tiếp Tục?") == true) {
        fetch('/api/pay_receipt_patient', {
            method: 'post',
            body: JSON.stringify({
                "id_phieukham": idphieukham,
                "id_tienkham" : id_tienkham,
                "tongtien_hoadon": tongtien_hoadon
            }),
             headers: {
                        'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
             if(data.code == 200)
             {
                alert("Thanh Toán Hóa Đơn Bệnh Nhân Thành Công !!")
                window.location.replace("/xemdanhsachkhambenh_bacsi")
                }
             else if( data.code == 400)
                     alert(data.err_msg)

        }).catch(err => console.error(err))
    }
}