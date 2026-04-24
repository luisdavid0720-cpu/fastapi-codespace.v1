<script>
  import { onMount, tick } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'
  import Badge from './Badge.svelte'
  import Modal from './Modal.svelte'
  import FormField from './FormField.svelte'

  import DataTable from 'simple-datatables'
  import 'simple-datatables/dist/style.css'

  let tabla
  let dataTable

  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list')
  let selected = $state(null)
  let saving = $state(false)
  let deleting = $state(false)
  let toastMsg = $state('')
  let editForm = $state(null)
  let generando = $state(false)

  let modalEliminarAbierto = $state(false)
  let pqrAEliminar = $state(null)

  let coordForm = $state({
    id_estado: '',
    respuesta: '',
    id_responsable: ''
  })

  let searchText = $state('')
  let filterEstado = $state('')
  let filterTipo = $state('')
  let filterDesde = $state('')
  let filterHasta = $state('')

  let tipos = $state([])
  let estados = $state([])
  let departamentos = $state([])
  let prioridades = $state([])
  let usuarios = $state([])

  let formDescripcion = $state('')
  let formIdTipo = $state('')
  let formIdDepartamento = $state('')

  function defaultForm() {
    formDescripcion = ''
    formIdTipo = ''
    formIdDepartamento = ''
    return {
      descripcion: '',
      id_tipo: '',
      id_departamento: ''
    }
  }

  let form = $state(defaultForm())

  let isAdmin = $derived($currentUser?.id_rol === 3)
  let isCoord = $derived($currentUser?.id_rol === 4)
  let isUser = $derived($currentUser?.id_rol === 1)

  let filtered = $derived(
    pqrs
      .filter((p) => {
        const belongsToMe =
          isAdmin ||
          isCoord ||
          Number(p.id_usuario) === Number($currentUser?.id_usuario)

        const matchText =
          !searchText ||
          p.descripcion?.toLowerCase().includes(searchText.toLowerCase())

        const matchEstado =
          !filterEstado ||
          String(p.id_estado) === String(filterEstado)

        const matchTipo =
          !filterTipo ||
          String(p.id_tipo) === String(filterTipo)

        const fecha = new Date(p.fecha)

        const matchDesde =
          !filterDesde || fecha >= new Date(filterDesde)

        const matchHasta =
          !filterHasta ||
          fecha <= new Date(filterHasta + 'T23:59:59')

        return (
          belongsToMe &&
          matchText &&
          matchEstado &&
          matchTipo &&
          matchDesde &&
          matchHasta
        )
      })
      .sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
  )

  onMount(async () => {
    await cargarDatos()
  })

  async function cargarDatos() {
    loading = true

    try {
      const [p, t, e, d, pr, u] = await Promise.allSettled([
        api.getPqrs(),
        api.getTiposPqr(),
        api.getEstados(),
        api.getDepartamentos(),
        api.getPrioridades(),
        api.getUsuarios()
      ])

      pqrs =
        p.status === 'fulfilled'
          ? p.value?.resultado || p.value || []
          : []

      tipos =
        t.status === 'fulfilled'
          ? t.value?.resultado || t.value || []
          : []

      estados =
        e.status === 'fulfilled'
          ? e.value?.resultado || e.value || []
          : []

      departamentos =
        d.status === 'fulfilled'
          ? d.value?.resultado || d.value || []
          : []

      prioridades =
        pr.status === 'fulfilled'
          ? pr.value?.resultado || pr.value || []
          : []

      usuarios =
        u.status === 'fulfilled'
          ? u.value?.resultado || u.value || []
          : []

      await tick()
      iniciarTabla()
    } catch (error) {
      console.error(error)
      showToast('❌ Error cargando datos')
    } finally {
      loading = false
    }
  }

  async function iniciarTabla() {
    await tick()

    if (!tabla) return

    if (dataTable) {
      dataTable.destroy()
      dataTable = null
    }

    dataTable = new DataTable(tabla, {
      searchable: true,
      fixedHeight: true,
      perPage: 10,
      perPageSelect: [5, 10, 15, 20],
      labels: {
        placeholder: 'Buscar...',
        perPage: '{select} registros por página',
        noRows: 'No hay registros',
        info: 'Mostrando {start} a {end} de {rows} registros'
      }
    })
  }

  function showToast(msg) {
    toastMsg = msg
    setTimeout(() => (toastMsg = ''), 3000)
  }

  function openCreate() {
    defaultForm()
    view = 'form'
  }

  function openDetail(pqr) {
    selected = pqr
    view = 'detail'
  }

  function openEdit(pqr) {
    editForm = { ...pqr }
    view = 'edit'
  }

  function openGestion(pqr) {
    selected = pqr
    coordForm = {
      id_estado: pqr.id_estado,
      respuesta: '',
      id_responsable: ''
    }
    view = 'gestion'
  }

  function pedirEliminar(pqr) {
    pqrAEliminar = pqr
    modalEliminarAbierto = true
  }

  async function deletePqr() {
    if (!pqrAEliminar) return

    deleting = true

    try {
      await api.deletePqr(pqrAEliminar.id_pqr)
      await cargarDatos()
      showToast('🗑️ Eliminado correctamente')
    } catch (error) {
      console.error(error)
      showToast('❌ Error eliminando')
    }

    deleting = false
  }

  const getLabelEstado = (id) =>
    estados.find((e) => e.id_estado == id)?.nombre || 'Pendiente'

  const getLabelTipo = (id) =>
    tipos.find((t) => t.id_tipo == id)?.nombre || '-'

  const getLabelUsuario = (id) =>
    usuarios.find((u) => u.id_usuario == id)?.nombre || `#${id}`
</script>

<Modal
  bind:abierto={modalEliminarAbierto}
  titulo="Eliminar"
  mensaje="¿Deseas eliminar este registro?"
  txtConfirm="Sí"
  txtCancel="Cancelar"
  peligroso={true}
  onconfirm={deletePqr}
/>

<div class="module">
  {#if toastMsg}
    <div class="toast">{toastMsg}</div>
  {/if}

  <header class="page-header">
    <h1>Gestión PQR</h1>

    {#if isUser}
      <button class="btn-create" onclick={openCreate}>
        + Crear PQR
      </button>
    {/if}
  </header>

  {#if view === 'list'}

    {#if loading}
      <p>Cargando...</p>
    {:else}

      <table bind:this={tabla} class="datatable">
        <thead>
          <tr>
            <th>ID</th>
            <th>Descripción</th>
            <th>Tipo</th>

            {#if isAdmin || isCoord}
              <th>Usuario</th>
              <th>Estado</th>
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
              <td>{getLabelTipo(pqr.id_tipo)}</td>

              {#if isAdmin || isCoord}
                <td>{getLabelUsuario(pqr.id_usuario)}</td>
                <td>
                  <Badge
                    texto={getLabelEstado(pqr.id_estado)}
                    id={pqr.id_estado}
                  />
                </td>
              {/if}

              <td>
                {new Date(pqr.fecha).toLocaleDateString('es-CO')}
              </td>

              <td>
                <button onclick={() => openDetail(pqr)}>
                  Ver
                </button>

                {#if isAdmin}
                  <button onclick={() => openEdit(pqr)}>
                    Editar
                  </button>

                  <button onclick={() => pedirEliminar(pqr)}>
                    Eliminar
                  </button>
                {/if}

                {#if isCoord}
                  <button onclick={() => openGestion(pqr)}>
                    Gestionar
                  </button>
                {/if}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>

    {/if}
  {/if}
</div>

<style>
  .module {
    padding: 30px;
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  .btn-create {
    background: #2563eb;
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    cursor: pointer;
  }

  .toast {
    position: fixed;
    right: 20px;
    bottom: 20px;
    background: #111827;
    color: white;
    padding: 12px 18px;
    border-radius: 10px;
  }

  table button {
    margin: 2px;
    padding: 5px 10px;
    cursor: pointer;
  }
</style>