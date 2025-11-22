
let show_movements = new XMLHttpRequest();
let buyPetition = new XMLHttpRequest();
let tradePetition = new XMLHttpRequest();





function movements(){
    show_movements.open("GET","/api/v1/movimientos");
    show_movements.onload = show_movements_handler;
    show_movements.onerror = function(){alert("No se ha podido completar la peticion de movimientos");};
    show_movements.send();
}

function showPurchaseModal() {
    
    const modalElement = document.getElementById('purchaseModal');
    
    const modal = new bootstrap.Modal(modalElement);
    
    modal.show();
}
function hidePurchaseModal() {
    
    const modalElement = document.getElementById('purchaseModal');
    
   
    const modal = bootstrap.Modal.getInstance(modalElement);
    
    modal.hide();
    
    
    
}


function get_exchange() {
    const coin_from = (document.getElementById("moneda_from_form") || {}).value;
    const coin_to   = (document.getElementById("moneda_to_form")   || {}).value;
    const amount_from = (document.getElementById("amount_from_form") || {}).value;
    
    if (!coin_from || !coin_to || !amount_from) {
        alert("Por favor completa todos los campos antes de calcular.");
        return;
    }
    
    if (coin_from === "EUR" && Number(amount_from) < 0.1){
        alert("Lo sentimos. Cantidad minina para comprar monedas : 0.10 Eur");
        return;
    } 
    
    if (coin_from === coin_to) {
        alert("Por favor seleccione dos monedas distintas.");
        return;
    }
    if ( Number(amount_from) < 0 || Number(amount_from) === 0){
        alert("Seleccione una cantidad mayor que 0")
        return;
    }
    
        const amountNumf = formatearNumeroServer(amount_from);
    
    const url = `/api/v1/tasa/${encodeURIComponent(coin_from)}/${encodeURIComponent(coin_to)}?amount=${encodeURIComponent(amountNumf)}`;
    const exchangePetition = new XMLHttpRequest();
    exchangePetition.open("GET", url, true);
    exchangePetition.onload = function () {
        if (exchangePetition.status >= 200 && exchangePetition.status < 300) {
            try {
                const data = JSON.parse(exchangePetition.responseText);
                const purchased = data.purchasedAmount ?? null;
                if (purchased === null) {
                    console.error("Fallo en la respuesta del servidor. Comprobar endpoint", data);
                    alert("Fallo en la respuesta del servidor. Comprobar endpoint");
                    return;
                }
                const out_data = document.getElementById("amount_to");
                out_data.value = purchased;
               
                
                  
                
                if (data.status === "Not Completed") {
                    let btn = document.getElementById("purchaseBtn");
                    btn.textContent = ("Try Again!");
                    btn.disabled = true;
                } else {
                    let btn = document.getElementById("purchaseBtn");
                    btn.textContent = ("Purchase!");
                    btn.disabled = false;
                    btn.addEventListener("click", buyMovement);
                }
                purchaseModal();
                showPurchaseModal();
            } catch (err) {
                console.error("Error transformando json JSON:", err, exchangePetition.responseText);
                alert("Respuesta inválida del servidor");
            }
        } else {
            console.error("Petición fallida:", exchangePetition.status, exchangePetition.statusText);
            
            try {
                const serverError = JSON.parse(exchangePetition.responseText);
                alert("Error servidor: " + (serverError.mensaje || exchangePetition.status));
            } catch (e) {
                alert("Error en la petición al servidor: " + exchangePetition.status);
            }
        }
    };
    exchangePetition.onerror = function () {
        console.error("Error de red");
        alert("No se pudo conectar con el servidor.");
    };
    
    exchangePetition.send();
}




function show_movements_handler(){
    if(this.readyState === 4){
        if(this.status === 200){
            
            const movimientos = JSON.parse(this.responseText);
            const datos = movimientos.datos;
            
           

            if (datos.length===0){
                
                let tabla = document.getElementById("movements_table");

                const fila = document.createElement("tr");

                const celda_vacia = document.createElement("td");
                celda_vacia.innerHTML = "No hay registros de movimientos.";
                fila.appendChild(celda_vacia);
                tabla.appendChild(fila);

            }else{

                let tabla = document.getElementById("movements_table");

                for( let i = 0; i < datos.length; i++){

                    const fila = document.createElement("tr");

                    const celda_time = document.createElement("td");
                    celda_time.innerHTML = datos[i][0];
                    fila.appendChild(celda_time);

                    const celda_moneda_from = document.createElement("td");
                    celda_moneda_from.innerHTML = datos[i][1];
                    fila.appendChild(celda_moneda_from);

                    const celda_amount_from = document.createElement("td");
                    celda_amount_from.innerHTML = formatearNUmeroCliente(datos[i][2]);
                    fila.appendChild(celda_amount_from);

                    const celda_moneda_to = document.createElement("td");
                    celda_moneda_to.innerHTML = datos[i][3];
                    fila.appendChild(celda_moneda_to);

                    const celda_amount_to = document.createElement("td");
                    celda_amount_to.innerHTML = formatearNUmeroCliente(datos[i][4]);
                    fila.appendChild(celda_amount_to);

                    const celda_unit_price = document.createElement("td");
                    celda_unit_price.innerHTML = formatearNUmeroCliente(datos[i][5])+"€";
                    fila.appendChild(celda_unit_price);

                    tabla.appendChild(fila);

                }

            }

        }else{
            alert("Se ha producido un error en la consulta http")
        }
    }
}

function viewForm() {
const form = document.getElementById('conversion_form');
form.classList.toggle('d-none');
}


function buyMovement(){
    const moneda_from = document.getElementById('moneda_from_form').value;
    const amount_from = formatearNumeroServer(document.getElementById('amount_from_form').value);
    const moneda_to = document.getElementById("moneda_to_form").value;
    const amount_to = document.getElementById('amount_to').value;

    
    

    buyPetition.open("POST","/api/v1/compra");
    buyPetition.onload = buyMovement_handler  
    buyPetition.onerror = function(){alert("Fallo al conectar con el servidor");};
    buyPetition.setRequestHeader("Content-Type","application/json")  

    
    const data_json = JSON.stringify(
        {
        "moneda_to":moneda_to,
        "amount_from":amount_from,
        "moneda_from":moneda_from,
        "amount_to":amount_to,
        }
        
    );
    
    buyPetition.send( data_json );
}
    
    
    

function status_info() {
    let invested = document.getElementById("invested_info");
    let recovered = document.getElementById("recovered_info");
    let valor_compra = document.getElementById("valor_compra_info");
    let wallet_value = document.getElementById("wallet_value");
    let diference = document.getElementById("diference")
    const statusPetition = new XMLHttpRequest();

    statusPetition.open("GET","/api/v1/status");
    statusPetition.onload = function () {
        const data = JSON.parse(statusPetition.responseText);
        if(Number(data.diference) == 0){
            diference.style.display = "none";
        }


        if (parseFloat(data.diference ?? 0) > 0){
           diference.textContent = formatearNUmeroCliente(data.diference) +"%" + "🠉";
           diference.style.color = "green";
        }else{
        diference.textContent = formatearNUmeroCliente(data.diference) +"%" + "🠋";  
        diference.style.color = "red";
        }


        invested.textContent = formatearNUmeroCliente(data.invested) +"€";
        recovered.textContent = formatearNUmeroCliente(data.recovered) +"€";
        valor_compra.textContent = formatearNUmeroCliente(data.valorCompra) +"€";
        wallet_value.textContent = formatearNUmeroCliente(data.wallet) +"€";
        
    };
    statusPetition.onerror = function () {
        alert("No se ha podido recuperar el estado de inversion");
    };
    statusPetition.send();
}
        

function buyMovement_handler(){
    if(this.readyState === 4){
        if(this.status === 200){
           answer = JSON.parse(this.responseText);

            alert(answer.message)
            cleanModal();
            location.reload();
        }else{
            alert("Se ha producido un error al intentar registrar el movimiento");
        }
    }
}
           

function cleanModal() {
    
    const moneda_from = document.getElementById('moneda_from_form');
    const amount_from = document.getElementById('amount_from_form');
    const moneda_to = document.getElementById('moneda_to_form');
    const amount_to = document.getElementById('amount_to');
    
    const model_moneda_from = document.getElementById("coin_from_modal");
    const model_amount_from = document.getElementById("amount_from_modal");
    const model_moneda_to = document.getElementById("coin_to_modal");
    const model_amount_to = document.getElementById("amount_to_modal");

    
    
    model_moneda_from.textContent = '';
    model_amount_from.value = 0;
    model_moneda_to.textContent = '';
    model_amount_to.value = 0;

    moneda_from.value = "";
    amount_from.value = "";
    moneda_to.value = "";
    amount_to.value = "";

}
function purchaseModal() {
    // Valores del formulario
    const moneda_from = document.getElementById('moneda_from_form').value;
    const amount_from = document.getElementById('amount_from_form').value;
    const moneda_to = document.getElementById('moneda_to_form').value;
    const amount_to = document.getElementById('amount_to').value;

    // Los del modal
    const model_moneda_from = document.getElementById("coin_from_modal");
    const model_amount_from = document.getElementById("amount_from_modal");
    const model_moneda_to = document.getElementById("coin_to_modal");
    const model_amount_to = document.getElementById("amount_to_modal");
    if(model_amount_to )
    // Limpieza de modal
    model_moneda_from.textContent = '';
    model_amount_from.textContent = '';
    model_moneda_to.textContent = '';
    model_amount_to.textContent = '';
    
    // Rellenado d modal
    let valor = Number(amount_to)
    if (Number.isNaN(valor)){
        model_amount_to.textContent = (amount_to);

    }else{
        
        model_amount_to.textContent = formatearNUmeroCliente(amount_to) + " " + moneda_to;
    }

    
    model_moneda_from.textContent = moneda_from;
    model_amount_from.textContent = formatearNUmeroCliente(amount_from) + " " + moneda_from;
    model_moneda_to.textContent = moneda_to;
}
  


function formatearNUmeroCliente(input) {
    const inputStr = String(input).trim();
    
    //Ultima pos de separador
    const lastCommaIndex = inputStr.lastIndexOf(',');
    const lastDotIndex = inputStr.lastIndexOf('.');
    const lastSeparatorIndex = Math.max(lastCommaIndex, lastDotIndex);
    
    let parteEntera, parteDecimal;
    
    if (lastSeparatorIndex !== -1) {
        // si hay decimal
        parteEntera = inputStr.substring(0, lastSeparatorIndex).replace(/[.,]/g, '');
        parteDecimal = inputStr.substring(lastSeparatorIndex + 1);
    } else {
        
        parteEntera = inputStr.replace(/[.,]/g, '');
        parteDecimal = '';
    }
    
    
    

    
    if (parteDecimal.length > 7) {
        const first7 = parteDecimal.slice(0, 7);
        const siguiente = parteDecimal[8];

        if (siguiente >= '5') {
            //redondeo
            let redondeada = String(Number(first7) + 1);
            redondeada = redondeada.padStart(7, '0');
            parteDecimal = redondeada;
        } else {
            
            parteDecimal = first7;
        }
    }

    //formateo de los miles
    let parteEnteraFormateada = '';
    for (let i = parteEntera.length - 1, contador = 0; i >= 0; i--, contador++) {
        if (contador > 0 && contador % 3 === 0) {
            parteEnteraFormateada = ',' + parteEnteraFormateada;
        }
        parteEnteraFormateada = parteEntera[i] + parteEnteraFormateada;
    }
    //reconstruccion
    if (parteDecimal) {
        return parteEnteraFormateada + '.' + parteDecimal;
    } else {
        return parteEnteraFormateada;
    }
}
            


    


function formatearNumeroServer(input_amount) {
    let amount = input_amount.trim();
    
    let formateado = "";
    for (let i = amount.length - 1; i >= 0; i--){
        if (amount[i]===","){
            continue;
           
        }
        formateado += amount[i];
    }
    formateado = formateado.split("").reverse().join("");
    formateado = Number(formateado);
    if (!isFinite(formateado) || formateado <= 0) {
    alert("Introduce una cantidad válida mayor que 0.");
    return;
    }
    formateado = String(formateado)
    return formateado;
}
function amountInputController() {
    const input = document.getElementById("amount_from_form");

    input.addEventListener("input", () => {
        let valor = input.value;
        
        valor = valor.replace(/[^0-9.]/g, "");
        valor = valor.replace(/(\..*)\./g, "$1"); 
        
        let [entera, decimal] = valor.split(".");
        
        entera = entera.replace(/^0+(?=\d)/, ""); 
        
        if (entera === "") entera = "0";
        entera = entera.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        valor = decimal !== undefined ? entera + "." + decimal : entera;
        input.value = valor;
    });
}

function allIn() {
    let selectWalletValue = document.getElementById("moneda_from_form");
    let allInBtn = document.getElementById("allInBtn");
    let amountFromInput = document.getElementById("amount_from_form");
    
    let coinWallet = 0;
    
    selectWalletValue.addEventListener("change", function () {
        let option = this.options[this.selectedIndex];
        coinWallet = option.dataset.wallet;
        if (coinWallet === undefined || coinWallet === "" || coinWallet === null) {
                allInBtn.disabled = true;
            } else {
                allInBtn.disabled = false;
        }
    });
    allInBtn.addEventListener("click", () => {
        amountFromInput.value = coinWallet;
    });
}
        


window.onload = function(){
   
    movements();
    amountInputController();
    allIn();
    status_info();
    
    
    let boton = document.getElementById("formBtn");
    boton.addEventListener("click",viewForm);
    
    let close_modal = document.getElementById("modal_close_btn")
    close_modal.addEventListener("click", cleanModal)
    let close_modal2 = document.getElementById("modal_close_btn2")
    close_modal2.addEventListener("click", cleanModal)
    const conversionButton = document.getElementById("conversion_button");
    conversionButton.addEventListener("click", get_exchange);
   
};

















