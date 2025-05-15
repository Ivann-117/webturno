document.addEventListener('DOMContentLoaded', () => {
    let editingRow = null;

    // Editar fila
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => {       
            if (editingRow) cancelEdit();
            editingRow = btn.closest('tr');
            editingRow.classList.add('editing');
            ['doc', 'nombre', 'apellido1', 'apellido2', 'rol'].forEach(cls => {
                const cell = editingRow.querySelector(`.${cls}`);
                const value = cell.innerText.trim();
                const input = document.createElement('input');
                input.value = value;
                input.className = 'form-control form-control-sm';
                input.name = cls;
                cell.innerText = '';
                cell.appendChild(input);
                input.focus();
            });
            document.getElementById('saveCancelGroup').classList.remove('d-none');
        });
    });
    // Eliminar fila
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const row = btn.closest('tr');
        const id = row.dataset.id;

        if (confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
            fetch('/admin_delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id })
            })
            .then(res => res.json())
            .then(json => {
                if (json.success) {
                    const toast = new bootstrap.Toast(document.getElementById('successToast'));
                    toast.show();
                    row.remove();  // Elimina la fila de la tabla directamente sin recargar
                } else {
                    alert('Error al eliminar: ' + (json.error || ''));
                }
            })
            .catch(err => {
                console.error('Error en fetch:', err);
                alert('Error en la conexión');
            });
        }
    });
});
    // Cancelar edición
    document.getElementById('cancelEdit').addEventListener('click', () => {
        cancelEdit();
    });

    // Guardar cambios
    document.getElementById('saveChanges').addEventListener('click', () => {
        if (!editingRow) return;
        const id = editingRow.dataset.id;
        const data = { id };
        ['doc', 'nombre', 'apellido1', 'apellido2', 'rol'].forEach(cls => {
            data[cls] = editingRow.querySelector(`.${cls} input`).value;
        });

        fetch('/admin_update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(json => {
            if (json.success) {
                const toast = new bootstrap.Toast(document.getElementById('successToast'));
                toast.show();
                setTimeout(() => window.location.reload(), 1500);
            } else {
                alert('Error al actualizar');
            }
        });
    });

    // Cancelar función
    function cancelEdit() {
        if (editingRow) {
            window.location.reload();
        }
    }

    // Filtros dinámicos (funciona ahora sí)
    const filtroDoc = document.getElementById('filtarDoc');
    const filtroNombre = document.getElementById('filtarNombre');
    const filtroApellido1 = document.getElementById('filtarApellido1');
    const filtroApellido2 = document.getElementById('filtarApellido2');
    const filtroRol = document.getElementById('filtarRol');
    const filtroEstado = document.getElementById('filtarEstado');

    const filtrarTabla = () => {
        const rows = document.querySelectorAll('#usersTable tbody tr');
        const valDoc = filtroDoc.value.toLowerCase();
        const valNombre = filtroNombre.value.toLowerCase();
        const valApellido1 = filtroApellido1.value.toLowerCase();
        const valApellido2 = filtroApellido2.value.toLowerCase();
        const valRol = filtroRol.value.toLowerCase();
        const valEstado = filtroEstado.value.toLowerCase();

        rows.forEach(row => {
            const doc = row.querySelector('.doc')?.textContent.toLowerCase() || '';
            const nombre = row.querySelector('.nombre')?.textContent.toLowerCase() || '';
            const apellido1 = row.querySelector('.apellido1')?.textContent.toLowerCase() || '';
            const apellido2 = row.querySelector('.apellido2')?.textContent.toLowerCase() || '';
            const rol = row.querySelector('.rol')?.textContent.toLowerCase() || '';
            const estado = row.querySelector('.estado')?.textContent.toLowerCase() || '';

            const match =
                doc.includes(valDoc) &&
                nombre.includes(valNombre) &&
                apellido1.includes(valApellido1) &&
                apellido2.includes(valApellido2) &&
                rol.includes(valRol) &&
                estado.includes(valEstado);

            row.style.display = match ? '' : 'none';
        });
    };

    [filtroDoc, filtroNombre, filtroApellido1, filtroApellido2, filtroRol, filtroEstado].forEach(input => {
        input.addEventListener('input', filtrarTabla);
    });
});
