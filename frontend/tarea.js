const tarea={template:`
<div>

<button type="button"
class="btn btn-primary fload-end"
data-bs-toggle="modal"
data-bs-target="#exampleModal"
@click="addClick()">
 Nueva Tarea
</button>

<h2></h2>

<div class="input-group mb-3">
    <span class="input-group-text">Orden</span>
    <select class="form-select" v-model="TareasOrden">
        <option value="0">Ascendente</option>
        <option value="1">Descendente</option>
    </select>
    <span class="input-group-text">Límite</span>
    <input type="number" class="form-control" v-model="TareasLimite">
    <button class="btn btn-secondary " type="button" id="button-addon2" @click="refreshData()">Aplicar</button>
    <button class="btn btn-secondary " type="button" id="button-addon2" @click="clearFilter()">Limpiar</button>
</div>

<table class="table table-striped">
<thead>
    <tr>
        <th>
            Id
        </th>
        <th>
            Archivo
        </th>
        <th>
            Nuevo formato
        </th>
        <th>
            Fecha solicitud
        </th>
        <th>
            Estado
        </th>
        <th>
            Opciones
        </th>
    </tr>
</thead>
<tbody>
    <tr v-for="dep in tareas">
        <td>{{dep.id}}</td>
        <td>{{dep.fileName}}</td>
        <td>{{dep.newFormat.llave}}</td>
        <td>{{dep.timeStamp}}</td>
        <td>{{dep.status.llave}}</td>
        <td>
            <button type="button"
            class="btn btn-light mr-1"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
            @click="editClick(dep)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                </svg>
            </button>
            <button type="button" @click="deleteClick(dep.id)"
            class="btn btn-light mr-1">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                </svg>
            </button>

        </td>
    </tr>
</tbody>
</thead>
</table>


<div>
<button type="button"
class="btn btn-secondary m-2 fload-end"
@click="signupClick()">
 Cerrar sesión
</button>
</div>

<div class="modal fade" id="exampleModal" tabindex="-1"
    aria-labelledby="exampleModalLabel" aria-hidden="true">
<div class="modal-dialog modal-lg modal-dialog-centered">
<div class="modal-content">
    <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">{{modalTitle}}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"
        aria-label="Close"></button>
    </div>

    <div class="modal-body">

        <div class="mb-3" v-if="TareaId==0">
        <label for="formFile" class="form-label">Seleccionar archivo a comprimir</label>
        <!--input class="form-control" type="file" id="formFile" v-model="TareaName"-->
        <input class="form-control" type="file" id="formFile" ref="file" v-on:change="handleFileUpload()">
        </div>

        <div class="input-group mb-3" v-if="TareaId==0">
            <span class="input-group-text">Nuevo Formato</span>
            <select class="form-select" v-model="TareaNuevoFormato">
                <option value="ZIP">ZIP</option>
                <option value="SEVENZIP">SEVENZIP</option>
                <option value="TARBZ2">TARBZ2</option>
            </select>
        </div>

        <div class="input-group mb-3" v-if="TareaId!=0">
            <span class="input-group-text">Archivo</span>
            <input type="text" class="form-control" v-model="TareaName" readonly>
        </div>

        <div class="input-group mb-3" v-if="TareaId!=0">
            <span class="input-group-text">Nuevo formato</span>
            <input type="text" class="form-control" v-model="TareaNuevoFormato" readonly>
        </div>

        <div class="input-group mb-3" v-if="TareaId!=0">
            <span class="input-group-text">Fecha solicitud</span>
            <input type="text" class="form-control" v-model="TareaFecha" readonly>
        </div>

        <div class="input-group mb-3" v-if="TareaId!=0">
            <span class="input-group-text">Estado</span>
            <input type="text" class="form-control" v-model="TareaEstado" readonly>
        </div>

        <button type="button" @click="createClick()"
        v-if="TareaId==0" class="btn btn-primary">
        Crear tarea
        </button>

        <button type="button" class="btn btn-primary m-2 fload-end" @click="downloadFile('ORIGINAL')"
        v-if="TareaId!=0" class="btn btn-primary">
        Descargar original
        </button>

        <!--PROCESSED, UPLOADED-->
        <button type="button" class="btn btn-primary m-2 fload-end" @click="downloadFile('COMPRIMIDO')"
        v-if="TareaId!=0 && TareaEstado=='PROCESSED'" class="btn btn-primary">
        Descargar comprimido
        </button>

    </div>

</div>
</div>
</div>


</div>


`,

data(){
    return{
        tareas:[],
        modalTitle:"",
        TareaId:0,
        TareaName:"",
        TareaNuevoFormato:"",
        TareaEstado:"",
        TareaFecha:"",
        usuario:0,
        file:[],
        TareasOrden:"",
        TareasLimite:"",

        TareaNameFilter:"",
        TareaIdFilter:"",
        tareasWithoutFilter:[]
    }
},
methods:{
    handleFileUpload(){
        this.file = this.$refs.file.files[0];
    },
    refreshData(){
        const params = {}
        if (this.TareasOrden != "") { params.order = this.TareasOrden }
        if (this.TareasLimite != "") { params.max = this.TareasLimite }

        axios.get(variables.API_URL+"tasks",{params,
            headers: {
                'Authorization': 'Bearer '+ sessionStorage.getItem('access_token')
            }
        })
        .then((response)=>{
            this.tareas=response.data;
            this.tareasWithoutFilter=response.data;
        });
    },
    addClick(){
        this.modalTitle="Nueva tarea";
        this.TareaId=0;
        this.TareaName="";
        this.TareaNuevoFormato="";
        this.TareaEstado="";
        this.TareaFecha="";
        this.file=[];
        this.$refs.file=[];
    },
    editClick(dep){
        this.modalTitle="Detalles de la  tarea";
        this.TareaId=dep.id;
        this.TareaName=dep.fileName;
        this.TareaNuevoFormato=dep.newFormat.llave;
        this.TareaEstado=dep.status.llave;
        this.TareaFecha=dep.timeStamp;
    },
    createClick(){
        let formData = new FormData();
        formData.append("fileName", this.file);
        formData.append("newFormat", this.TareaNuevoFormato);

        const headers = {
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer '+ sessionStorage.getItem('access_token')
          }

        axios.post(variables.API_URL+"tasks", formData, {
            headers: headers
        })
        .then((response)=>{
            this.refreshData();
            //alert(response.data);
            alert("Tarea creada.");
        }).catch(function(error){
            alert(error.response.data)
        });
    },
    updateClick(){
        axios.put(variables.API_URL+"tasks/"+this.TareaId,{
            nombre:this.TareaName,
            categoria:this.TareaNuevoFormato
        },{
            headers: {
                'Authorization': 'Bearer '+ sessionStorage.getItem('access_token')
            }
        })
        .then((response)=>{
            this.refreshData();
            //alert(response.data);
            alert("Tarea modificada.");
        }).catch(function(error){
            alert(error.response.data)
        });
    },
    deleteClick(id){
        if(!confirm("Está seguro de eliminar la tarea?")){
            return;
        }
        axios.delete(variables.API_URL+"tasks/"+id,{
            headers: {
                'Authorization': 'Bearer '+ sessionStorage.getItem('access_token') 
            }
        }
        )
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        }).catch(function(error){
            alert(error.response.data)
        });
    },
    downloadFile(tipo_archivo){
        //axios.get(variables.API_URL+"files/"+"Cronograma_AML_202310.pdf",{ 
        if (tipo_archivo == 'COMPRIMIDO'){
            extension = ''
            if (this.TareaNuevoFormato == 'ZIP') {extension = 'zip'}
            else if (this.TareaNuevoFormato == 'SEVENZIP') {extension = '7z'}
            else if (this.TareaNuevoFormato == 'TARBZ2') {extension = 'tar.bz2'}
            download_filename = this.TareaName.split('.')[0] + '.' + extension //.toLowerCase()
        } else {
            download_filename = this.TareaName;
        }

        //download_filename = this.TareaName;
        axios.get(variables.API_URL+"files/"+download_filename,{
            headers: {
                'Authorization': 'Bearer '+ sessionStorage.getItem('access_token') 
            },
            responseType:'blob'
        }
        )
        .then((response)=>{
            var fileURL = window.URL.createObjectURL(new Blob([response.data]));
            var fileLink = document.createElement('a');
  
            fileLink.href = fileURL;
            //fileLink.setAttribute('download', 'Cronograma_AML_202310.pdf');
            fileLink.setAttribute('download', download_filename);
            document.body.appendChild(fileLink);
            fileLink.click();

        }).catch(async function(error){
            let res = await error.response.data.text() 
            alert(res)
            console.log(error.response.data)
        });
    },
    signupClick(){
        sessionStorage.setItem('usuario', 0);
        this.$router.push("/usuario");
    },
    clearFilter(){
        this.TareasOrden = "";
        this.TareasLimite = "";
        this.refreshData();
    }

},
mounted:function(){
    this.refreshData();
}

}