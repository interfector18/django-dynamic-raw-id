(function($) {
  $(document).ready(function($) {
    $('#changelist-filter .vForeignKeyRawIdAdminField').each(function() {
      const $input = $(this);
      $input.data('val', $input.val());
      setInterval(function() {
        if ($input.data('val') !== $input.val()) {
          const $form = $input.closest("form");
          $input.data('val', $input.val());
          if (!$input.val()) {
            $input.remove();
          }
          $form.submit();
        }
      }, 100);
    });
  });
})(django.jQuery);
