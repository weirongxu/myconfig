<?php
require_once(__DIR__.'/../plugins/login-password-less.php');

/** Set allowed password
 * @param string result of password_hash
 */
return new AdminerLoginPasswordLess(
    $password_hash = password_hash("admin", PASSWORD_DEFAULT)
);
