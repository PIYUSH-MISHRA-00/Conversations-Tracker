<?php
/*
Plugin Name: Call Management Plugin
Description: A professional call management plugin to handle call data with Excel file uploads.
Version: 1.0
Author: Your Name
*/

defined('ABSPATH') or die('No script kiddies please!');

// Enqueue scripts and styles
function cmp_enqueue_assets() {
    wp_enqueue_style('cmp-style', plugins_url('css/style.css', __FILE__));
    wp_enqueue_script('cmp-script', plugins_url('js/script.js', __FILE__), array('jquery'), null, true);
}
add_action('admin_enqueue_scripts', 'cmp_enqueue_assets');

// Add admin menu
function cmp_add_admin_menu() {
    add_menu_page(
        'Call Management',
        'Call Management',
        'manage_options',
        'call-management',
        'cmp_admin_page',
        'dashicons-phone'
    );
}
add_action('admin_menu', 'cmp_add_admin_menu');

// Admin page callback
function cmp_admin_page() {
    ?>
    <div class="wrap">
        <h1>Call Management Platform</h1>
        <form id="cmp-upload-form" method="post" enctype="multipart/form-data">
            <input type="file" name="cmp_excel_file" id="cmp_excel_file" accept=".xlsx">
            <input type="submit" name="cmp_upload" value="Upload File" class="button button-primary">
        </form>
        <div id="cmp-results">
            <?php cmp_handle_file_upload(); ?>
        </div>
    </div>
    <?php
}

// Handle file upload and data processing
function cmp_handle_file_upload() {
    if (isset($_POST['cmp_upload']) && !empty($_FILES['cmp_excel_file']['name'])) {
        require_once plugin_dir_path(__FILE__) . 'vendor/autoload.php';
        use PhpOffice\PhpSpreadsheet\IOFactory;
        
        $file = $_FILES['cmp_excel_file']['tmp_name'];
        $spreadsheet = IOFactory::load($file);
        $worksheet = $spreadsheet->getActiveSheet();
        $data = $worksheet->toArray();

        $header = array_shift($data);
        $columns = array_map('strtolower', $header);
        $phone_col = array_search('phone number', $columns);
        if ($phone_col === false) {
            $phone_col = array_search('phone', $columns);
        }
        if ($phone_col === false) {
            $phone_col = array_search('mobile number', $columns);
        }
        if ($phone_col === false) {
            $phone_col = array_search('contact', $columns);
        }
        if ($phone_col === false) {
            echo "<div class='notice notice-error'><p>Error: No valid 'Phone Number' column found in the file.</p></div>";
            return;
        }

        $results = [];
        foreach ($data as $row) {
            $results[] = [
                'Phone Number' => $row[$phone_col],
                'Called' => isset($row[$phone_col + 1]) && strtolower($row[$phone_col + 1]) == 'yes',
                'Notes' => isset($row[$phone_col + 2]) ? $row[$phone_col + 2] : ''
            ];
        }

        $_SESSION['cmp_data'] = $results;
        ?>
        <div class="cmp-data-container">
            <table class="cmp-data-table">
                <thead>
                    <tr>
                        <th>Phone Number</th>
                        <th>Called</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($results as $index => $row): ?>
                        <tr>
                            <td><?php echo esc_html($row['Phone Number']); ?></td>
                            <td><input type="checkbox" class="cmp-called-checkbox" data-index="<?php echo $index; ?>" <?php echo $row['Called'] ? 'checked' : ''; ?>></td>
                            <td><input type="text" class="cmp-notes-input" data-index="<?php echo $index; ?>" value="<?php echo esc_attr($row['Notes']); ?>"></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
            <button id="cmp-save-button" class="button button-primary">Save Changes</button>
            <a href="<?php echo esc_url(admin_url('admin-post.php?action=cmp_download_file')); ?>" class="button button-secondary">Download Updated Data</a>
        </div>
        <?php
    }
}

// Handle data saving
function cmp_save_changes() {
    if (isset($_POST['cmp_data'])) {
        $_SESSION['cmp_data'] = json_decode(stripslashes($_POST['cmp_data']), true);
        wp_send_json_success('Data saved.');
    }
    wp_send_json_error('Error saving data.');
}
add_action('wp_ajax_cmp_save_changes', 'cmp_save_changes');

// Handle file download
function cmp_download_file() {
    if (!isset($_SESSION['cmp_data'])) {
        wp_die('No data available.');
    }
    
    require_once plugin_dir_path(__FILE__) . 'vendor/autoload.php';
    use PhpOffice\PhpSpreadsheet\Spreadsheet;
    use PhpOffice\PhpSpreadsheet\Writer\Xlsx;
    
    $spreadsheet = new Spreadsheet();
    $sheet = $spreadsheet->getActiveSheet();
    $data = $_SESSION['cmp_data'];

    // Write header
    $sheet->setCellValue('A1', 'Phone Number');
    $sheet->setCellValue('B1', 'Called');
    $sheet->setCellValue('C1', 'Notes');

    // Write data
    $rowNumber = 2;
    foreach ($data as $row) {
        $sheet->setCellValue('A' . $rowNumber, $row['Phone Number']);
        $sheet->setCellValue('B' . $rowNumber, $row['Called'] ? 'Yes' : 'No');
        $sheet->setCellValue('C' . $rowNumber, $row['Notes']);
        $rowNumber++;
    }

    $writer = new Xlsx($spreadsheet);
    $filename = 'updated_call_data.xlsx';
    $tempFile = tempnam(sys_get_temp_dir(), $filename);
    $writer->save($tempFile);

    header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    header('Content-Disposition: attachment;filename="' . $filename . '"');
    header('Cache-Control: max-age=0');
    readfile($tempFile);
    unlink($tempFile);
    exit;
}
add_action('admin_post_cmp_download_file', 'cmp_download_file');

?>
