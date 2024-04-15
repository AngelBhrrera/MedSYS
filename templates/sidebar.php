<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Topbar</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
   <!-- Barra lateral -->
    <div class="sidebar">
        <h3>Menu</h3>
        <ul>
            <li><a href="placeholder.php">Citas</a></li>
            <li><a href="placeholder.php">Pacientes</a></li>
            <?php
            $tipo_usuario = 0; // Por defecto, asumimos que es un administrador
            // Puedes cambiar el valor de $tipo_usuario según el tipo de usuario que haya iniciado sesión
            // Esto es provisional, se cambiara cuando ya se manejen sesiones

            if ($tipo_usuario == 0 || $tipo_usuario == 1) {
                // Si es un administrador o un doctor, mostrar estas opciones
                echo '<li><a href="placeholder">Consulta</a></li>';
            }

            if ($tipo_usuario == 0) {
                // Si es un administrador, mostrar estas opciones adicionales
                echo '<li><a href="placeholder">Gestión de Usuarios</a></li>';
                echo '<li><a href="placeholder">Gestión de Enfermedades</a></li>';
                echo '<li><a href="placeholder">Gestión de Síntomas</a></li>';
                echo '<li><a href="placeholder">Gestión de Signos</a></li>';
            }
            ?>

        </ul>
    </div>
</body>
</html>