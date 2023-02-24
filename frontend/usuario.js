const usuario={template:`
<div>

<div class="p-2 w-50 bd-highlight">
    <div class="input-group mb-3">
        <span class="input-group-text">Usuario</span>
        <input type="text" class="form-control" v-model="UsuarioNombre">
    </div>

    <div class="input-group mb-3">
        <span class="input-group-text">Contraseña</span>
        <input type="password" class="form-control" v-model="UsuarioContrasena">
    </div>

</div>

<button type="button"
class="btn btn-primary m-2 fload-end"
@click="loginClick()">
 Iniciar sesión
</button>

<button type="button"
class="btn btn-secondary m-2 fload-end"
data-bs-toggle="modal"
data-bs-target="#exampleModal"
@click="addClick()">
 Registrarse
</button>


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
    
        <div class="input-group mb-3">
            <span class="input-group-text">Nombre</span>
            <input type="text" class="form-control" v-model="NuevoUsuarioNombre">
        </div>

        <div class="input-group mb-3">
            <span class="input-group-text">Email</span>
            <input type="text" class="form-control" v-model="NuevoUsuarioEmail">
        </div>

        <div class="input-group mb-3">
            <span class="input-group-text">Contraseña</span>
            <input type="password" class="form-control" v-model="NuevoUsuarioContrasena1">
        </div>

        <div class="input-group mb-3">
            <span class="input-group-text">Confirmar contraseña</span>
            <input type="password" class="form-control" v-model="NuevoUsuarioContrasena2">
        </div>

        <button type="button" @click="createClick()"
        v-if="UsuarioId==0" class="btn btn-primary">
        Registrarse
        </button>

        <button type="button" @click="updateClick()"
        v-if="UsuarioId!=0" class="btn btn-primary">
        Actualizar usuario
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
        usuarios:[],
        modalTitle:"",
        UsuarioId:0,
        UsuarioNombre:"",
        UsuarioEmail:"",
        UsuarioContrasena:"",
        usuario:[]
    }
},
methods:{
    refreshData(){
        /*axios.get(variables.API_URL+"usuario")
        .then((response)=>{
            this.usuarios=response.data;
        });

        axios.get(variables.API_URL+"tarea")
        .then((response)=>{
            this.tareas=response.data;
        });*/
    },
    loginClick(){
        axios.post(variables.API_URL+"auth/login",{
            username:this.UsuarioNombre,
            password:this.UsuarioContrasena
        })
        .then((response)=>{
            //this.refreshData();
            sessionStorage.setItem('access_token', response.data.token_de_acceso);
            //alert(response.data);
            this.usuario=response.data
            this.$router.push("/tarea");
        }).catch(function(error){
            alert(error.response.data)
        });
    },
    addClick(){
        this.modalTitle="Nuevo usuario";
        this.NuevoUsuarioId=0;
        this.NuevoUsuarioNombre="";
        this.NuevoUsuarioEmail="",
        this.NuevoUsuarioContrasena=""
    },
    createClick(){
        axios.post(variables.API_URL+"auth/signup",{
            username:this.NuevoUsuarioNombre,
            email:this.NuevoUsuarioEmail,
            password1:this.NuevoUsuarioContrasena1,
            password2:this.NuevoUsuarioContrasena2
        })
        .then((response)=>{
            //this.refreshData();
            alert(response.data.mensaje);
        }).catch(function(error){
            alert(error.response.data)
        });
    }

},
mounted:function(){
    this.refreshData();
}

}