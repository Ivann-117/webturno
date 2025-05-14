document.addEventListener('DOMContentLoaded', () => {
    let editingRow = null;

    // Botones de edición
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (editingRow) cancelEdit();
            editingRow = btn.closest('tr');
            editingRow.classList.add('editing');
            ['doc', 'nombre', 'apellido1', 'apellido2', 'rol'].forEach(cls => {
                let cell = editingRow.querySelector(`.${cls}`);
                let val = cell.innerText.trim();
                let input = document.createElement('input');
                input.value = val;
                input.className = 'form-control form-control-sm';
                input.name = cls;
                cell.innerText = '';
                cell.appendChild(input);
                input.focus(); // Focaliza el campo de entrada
            });
            document.getElementById('saveCancelGroup').classList.remove('d-none');
        });
    });

    // Botón cancelar edición
    document.getElementById('cancelEdit').addEventListener('click', () => {
        cancelEdit();
    });

    // Botón guardar cambios
    document.getElementById('saveChanges').addEventListener('click', () => {
        if (!editingRow) return;
        let id = editingRow.dataset.id;
        let data = { id };
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
                // Mostrar notificación de éxito
                let successToast = new bootstrap.Toast(document.getElementById('successToast'));
                successToast.show();
                setTimeout(() => {
                    window.location.reload();
                }, 2000); // Recargar después de 2 segundos
            } else {
                alert('Error al actualizar');
            }
        });
    });

    // Cancelar edición
    function cancelEdit() {
        if (!editingRow) return;
        window.location.reload();
    }

    // Botón eliminar
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const row = btn.closest('tr');
            const id = row.dataset.id;

            // Confirmar la eliminación
            if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
                fetch('/admin_delete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id })
                })
                .then(res => res.json())
                .then(json => {
                    if (json.success) {
                        // Eliminar la fila de la tabla
                        row.remove();
                        alert('Usuario eliminado correctamente');
                    } else {
                        alert('Error al eliminar el usuario');
                    }
                });
            }
        });
    });
});
