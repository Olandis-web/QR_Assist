import flet as ft
from database import usuarios


def dialogo_cambiar_contrasena(page: ft.Page, id_usuario):
    """Muestra un dialogo (AlertDialog) que permite al empleado cambiar
    su propia contraseña, solicitando la contraseña actual como verificacion
    y la nueva contraseña como confirmacion."""

    contrasena_actual = ft.TextField(
        label="Contraseña actual",
        password=True,
        can_reveal_password=True,
    )

    contrasena_nueva = ft.TextField(
        label="Nueva contraseña",
        password=True,
        can_reveal_password=True,
    )

    contrasena_confirmar = ft.TextField(
        label="Confirmar nueva contraseña",
        password=True,
        can_reveal_password=True,
    )

    lbl_error = ft.Text("", color="red", size=13)

    def cerrar(e):
        dialog.open = False
        page.update()

    def confirmar(e):
        """Valida los campos y ejecuta el cambio de contraseña"""

        lbl_error.value = ""

        # Validaciones basicas de formulario
        if not contrasena_actual.value or not contrasena_nueva.value or not contrasena_confirmar.value:
            lbl_error.value = "Todos los campos son obligatorios"
            lbl_error.update()
            return

        if contrasena_nueva.value != contrasena_confirmar.value:
            lbl_error.value = "La nueva contraseña y la confirmación no coinciden"
            lbl_error.update()
            return

        if contrasena_nueva.value == contrasena_actual.value:
            lbl_error.value = "La nueva contraseña debe ser diferente a la actual"
            lbl_error.update()
            return

        # Verifica que la contraseña actual sea correcta
        es_valida = usuarios.verificar_contrasena(id_usuario, contrasena_actual.value)

        if not es_valida:
            lbl_error.value = "La contraseña actual es incorrecta"
            lbl_error.update()
            return

        # Actualiza la contraseña en la base de datos
        usuarios.cambiar_contrasena(id_usuario, contrasena_nueva.value)

        dialog.open = False
        page.update()

        snack = ft.SnackBar(
            content=ft.Text("Contraseña actualizada correctamente", color="white"),
            bgcolor="green",
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cambiar contraseña"),
        content=ft.Column(
            controls=[
                contrasena_actual,
                contrasena_nueva,
                contrasena_confirmar,
                lbl_error,
            ],
            tight=True,
            spacing=15,
            width=320,
        ),
        actions=[
            ft.ElevatedButton("Cancelar", color = "white", on_click=cerrar),
            ft.ElevatedButton("Confirmar", color = "white", bgcolor = "red", on_click=confirmar),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()