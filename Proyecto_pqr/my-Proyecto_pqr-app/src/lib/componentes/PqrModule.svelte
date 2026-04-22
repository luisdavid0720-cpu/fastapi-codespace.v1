<!-- PqrModule.svelte -->
<script>
import { onMount } from 'svelte'
import { currentUser } from '../../stores/auth.js'
import { api } from '../api.js'

let pqrs = $state([])
let loading = $state(true)
let view = $state('list')
let selected = $state(null)
let saving = $state(false)
let deleting = $state(false)
let toastMsg = $state('')
let editForm = $state(null)

let isAdmin = $derived($currentUser?.id_rol === 3)
let isCoordinador = $derived($currentUser?.id_rol === 4)
let isGestor = $derived(isAdmin || isCoordinador)

let form = $state({
descripcion:'',
id_tipo:'',
id_departamento:''
})

let tipos = $state([])
let estados = $state([])
let prioridades = $state([])
let departamentos = $state([])

onMount(async()=>{
await loadData()
})

async function loadData(){
loading=true
try{
const p = await api.getPqrs()
const t = await api.getTiposPqr()
const e = await api.getEstados()
const pr = await api.getPrioridades()
const d = await api.getDepartamentos()

pqrs = p.resultado || []
tipos = t || []
estados = e || []
prioridades = pr || []
departamentos = d || []
}catch(err){
console.error(err)
}
loading=false
}

let filtered = $derived(
pqrs.filter(p=>{
if(isGestor) return true
return Number(p.id_usuario) === Number($currentUser?.id_usuario)
})
)

function getTipo(id){
return tipos.find(x=>x.id_tipo==id)?.nombre || '-'
}

function getEstado(id){
return estados.find(x=>x.id_estado==id)?.nombre || '-'
}

function getPrioridad(id){
return prioridades.find(x=>x.id_prioridad==id)?.nombre || '-'
}

function getDepartamento(id){
return departamentos.find(x=>x.id_departamento==id)?.nombre || '-'
}

function showToast(msg){
toastMsg = msg
setTimeout(()=>toastMsg='',3000)
}

function openCreate(){
form = {
descripcion:'',
id_tipo:'',
id_departamento:''
}
view='form'
}

function openEdit(pqr){
editForm = {
id_pqr:pqr.id_pqr,
descripcion:pqr.descripcion,
id_tipo:pqr.id_tipo,
id_departamento:pqr.id_departamento,
id_estado:pqr.id_estado,
id_prioridad:pqr.id_prioridad,
respuesta:pqr.respuesta || ''
}
view='edit'
}

function openDetail(pqr){
selected = pqr
view='detail'
}

async function savePqr(){
saving=true
try{
await api.createPqr({
...form,
id_usuario:$currentUser.id_usuario,
id_estado:1,
id_prioridad:1,
fecha:new Date().toISOString()
})
showToast('PQRS creada')
await loadData()
view='list'
}catch(err){
showToast('Error al guardar')
}
saving=false
}

async function saveEdit(){
saving=true
try{

if(editForm.respuesta && editForm.id_estado == 1){
editForm.id_estado = 2
}

await api.updatePqr(editForm.id_pqr,editForm)
showToast('PQRS actualizada')
await loadData()
view='list'
}catch(err){
showToast('Error al actualizar')
}
saving=false
}

async function deletePqr(pqr){
if(!confirm('Eliminar PQRS?')) return

deleting=true
try{
await api.deletePqr(pqr.id_pqr)
showToast('Eliminada')
await loadData()
}catch(err){
showToast('Error al eliminar')
}
deleting=false
}
</script>

<div class="module">

{#if toastMsg}
<div class="toast">{toastMsg}</div>
{/if}

{#if view === 'list'}

<div class="header">
<h1>Gestión PQRS</h1>

{#if !isGestor}
<button class="btn-primary" onclick={openCreate}>
Nueva PQRS
</button>
{/if}
</div>

{#if loading}
<div class="loading">Cargando...</div>

{:else}

<div class="table-box">
<table>
<thead>
<tr>
<th>ID</th>
<th>Descripción</th>
<th>Tipo</th>

{#if isGestor}
<th>Departamento</th>
<th>Prioridad</th>
<th>Estado</th>
<th>Respuesta</th>
{/if}

<th>Fecha</th>
<th>Acciones</th>
</tr>
</thead>

<tbody>

{#each filtered as pqr}
<tr>
<td>#{pqr.id_pqr}</td>
<td>{pqr.descripcion}</td>
<td>{getTipo(pqr.id_tipo)}</td>

{#if isGestor}
<td>{getDepartamento(pqr.id_departamento)}</td>
<td>{getPrioridad(pqr.id_prioridad)}</td>
<td>{getEstado(pqr.id_estado)}</td>
<td>{pqr.respuesta || 'Pendiente'}</td>
{/if}

<td>{new Date(pqr.fecha).toLocaleDateString()}</td>

<td class="actions">

<button onclick={() => openDetail(pqr)}>
Ver
</button>

{#if isGestor}
<button onclick={() => openEdit(pqr)}>
Editar
</button>
{/if}

{#if isAdmin}
<button class="danger" onclick={() => deletePqr(pqr)}>
Eliminar
</button>
{/if}

</td>
</tr>
{/each}

</tbody>
</table>
</div>

{/if}

{:else if view === 'form'}

<div class="card">
<h2>Nueva PQRS</h2>

<textarea bind:value={form.descripcion} placeholder="Descripción"></textarea>

<select bind:value={form.id_tipo}>
<option value="">Tipo</option>
{#each tipos as t}
<option value={t.id_tipo}>{t.nombre}</option>
{/each}
</select>

<select bind:value={form.id_departamento}>
<option value="">Departamento</option>
{#each departamentos as d}
<option value={d.id_departamento}>{d.nombre}</option>
{/each}
</select>

<button class="btn-primary" onclick={savePqr} disabled={saving}>
Guardar
</button>

<button onclick={() => view='list'}>
Volver
</button>
</div>

{:else if view === 'edit'}

<div class="card">
<h2>Editar PQRS #{editForm.id_pqr}</h2>

<textarea bind:value={editForm.descripcion}></textarea>

<select bind:value={editForm.id_estado}>
{#each estados as e}
<option value={e.id_estado}>{e.nombre}</option>
{/each}
</select>

<select bind:value={editForm.id_prioridad}>
{#each prioridades as p}
<option value={p.id_prioridad}>{p.nombre}</option>
{/each}
</select>

<textarea bind:value={editForm.respuesta} placeholder="Respuesta coordinador"></textarea>

<button class="btn-primary" onclick={saveEdit} disabled={saving}>
Guardar cambios
</button>

<button onclick={() => view='list'}>
Volver
</button>
</div>

{:else if view === 'detail'}

<div class="card">
<h2>PQRS #{selected.id_pqr}</h2>

<p><b>Descripción:</b> {selected.descripcion}</p>
<p><b>Tipo:</b> {getTipo(selected.id_tipo)}</p>
<p><b>Estado:</b> {getEstado(selected.id_estado)}</p>
<p><b>Prioridad:</b> {getPrioridad(selected.id_prioridad)}</p>
<p><b>Respuesta:</b> {selected.respuesta || 'Pendiente'}</p>

<button onclick={() => view='list'}>
Volver
</button>
</div>

{/if}

</div>

<style>
.module{
padding:30px;
font-family:Inter,sans-serif;
}

.header{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:20px;
}

h1,h2{
margin:0 0 15px 0;
}

.btn-primary{
background:#2563eb;
color:white;
border:none;
padding:12px 18px;
border-radius:10px;
cursor:pointer;
font-weight:700;
}

.table-box{
background:white;
border-radius:14px;
overflow:auto;
box-shadow:0 5px 20px rgba(0,0,0,.05);
}

table{
width:100%;
border-collapse:collapse;
}

th,td{
padding:14px;
border-bottom:1px solid #eee;
text-align:left;
font-size:14px;
}

th{
background:#f8fafc;
}

.actions{
display:flex;
gap:8px;
}

.actions button{
padding:8px 12px;
border:none;
border-radius:8px;
cursor:pointer;
}

.danger{
background:#dc2626;
color:white;
}

.card{
max-width:700px;
background:white;
padding:25px;
border-radius:14px;
box-shadow:0 5px 20px rgba(0,0,0,.05);
display:flex;
flex-direction:column;
gap:14px;
}

textarea,select{
padding:12px;
border:1px solid #ddd;
border-radius:10px;
font-family:inherit;
}

textarea{
min-height:120px;
resize:none;
}

.toast{
position:fixed;
bottom:20px;
right:20px;
background:#111827;
color:white;
padding:14px 20px;
border-radius:10px;
z-index:999;
}

.loading{
padding:30px;
font-weight:700;
}
</style>