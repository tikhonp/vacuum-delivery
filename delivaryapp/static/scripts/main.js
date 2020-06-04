function updatestatus() {
		for (i in ActiveOrders) {
				var xhr = new XMLHttpRequest();

				xhr.open('GET', `http://127.0.0.1:8000/api/v1/order/${ActiveOrders[i]}/`, false);
				xhr.send();
				
				if (xhr.status != 200) {
					console.log(`Ошибка ${xhr.status}: ${xhr.statusText}`);
				}
				else {
						var response = JSON.parse(xhr.responseText);
						var hed = document.getElementById(`header_order${ActiveOrders[i]}`);	
						console.log(hed.innerHTML);
						if (response.is_active) { 
								if (hed.innerHTML == "Добавлен") {
										hed.innerHTML = "Выполняется";
										orderDiv = document.getElementById(`order${ActiveOrders[i]}`);
										orderDiv.classList.add("border-info");
										orderDiv.classList.add("mb-3");
								}
						}
						else {
								hrf = document.getElementById(`order_got${ActiveOrders[i]}`);
								if ((response.wuser != "None") && (hrf == null)) {
										console.log("okay");
										var a = document.createElement('a');
										a.href = `getorder?order=${ActiveOrders[i]}`;
										a.id = `order_got${ActiveOrders[i]}`;
										a.classList.add("btn");
										a.classList.add("btn-primary");
										a.innerHTML = "Я забрал заказ";
										var orderDiv = document.getElementById(`order${ActiveOrders[i]}`);
										orderDiv.appendChild(a);
										document.getElementById("activo").style.display = 'none';
										document.getElementById("activo").style.display = 'block';
								}
						}
				}
		}
}

setInterval(updatestatus, 2000);
