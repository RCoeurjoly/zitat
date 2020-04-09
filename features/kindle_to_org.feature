# -*- coding: utf-8 -*-
Feature: kindle generated clippings are converted to org mode

  Scenario: a single Kindle clippings should be converted to valid org mode
    Given the kindle generated clipping
    """
    Obras completas (Epicuro)
    - Your Highlight on Location 1186-1188 | Added on Friday, December 27, 2019 1:48:52 PM

    Acostúmbrate a pensar que la muerte no tiene nada que ver con nosotros, porque todo bien y todo mal radica en la sensación, y la muerte es la privación de sensación. De ahí que la idea correcta de que la muerte no tiene nada que ver con nosotros hace gozosa la mortalidad de la vida, no porque añada un tiempo infinito sino porque quita las ansias de inmortalidad.
    ==========

      """
    When we convert the clipping to org format
    Then we should get the org clipping
    """
    * Epicuro

    ** Obras completas

    *** Acostúmbrate a pensar que la muerte no tiene nada que ver --

    Acostúmbrate a pensar que la muerte no tiene nada que ver con nosotros, porque todo bien y todo mal radica en la sensación, y la muerte es la privación de sensación. De ahí que la idea correcta de que la muerte no tiene nada que ver con nosotros hace gozosa la mortalidad de la vida, no porque añada un tiempo infinito sino porque quita las ansias de inmortalidad.

    /Highlight on Location 1186-1188. [2019-12-27 13:48:52]./


      """
