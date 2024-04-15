<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Barra superior -->
    <?php include 'topbar.php'; ?>
    
    <!-- Contenido principal -->
    <div class="container">
        <!-- Barra lateral -->
        <?php include 'sidebar.php'; ?>

        <!-- Contenido principal -->
        <div class="main-content">
            <!-- Mensaje de bienvenida -->
            <h1>Bienvenido, [nombre del usuario]</h1>

            <!-- Próximas citas -->
            <h2>Sus próximas citas:</h2>
            <div class="citas">
                <!-- Recuadro de la primera cita -->
                <div class="cita">
                    <!-- Aquí puedes agregar detalles de la cita -->
                </div>

                <!-- Recuadro de la segunda cita -->
                <div class="cita">
                    <!-- Aquí puedes agregar detalles de la cita -->
                </div>

                <!-- Recuadro de la tercera cita -->
                <div class="cita">
                    <!-- Aquí puedes agregar detalles de la cita -->
                </div>
            </div>
        </div>
    </div>
</body>
</html>

