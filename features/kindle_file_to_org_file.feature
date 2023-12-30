# -*- coding: utf-8 -*-
Feature: kindle generated clippings files are converted to org mode files

  Scenario: a single Kindle clippings should be converted to valid org mode
    Given the kindle generated clipping file "My Clippings.txt" whose content is
      """
      Obras completas (Epicuro)
      - Your Highlight on Location 1186-1188 | Added on Friday, December 27, 2019 1:48:52 PM

      Acostúmbrate a pensar que la muerte no tiene nada que ver con nosotros, porque todo bien y todo mal radica en la sensación, y la muerte es la privación de sensación. De ahí que la idea correcta de que la muerte no tiene nada que ver con nosotros hace gozosa la mortalidad de la vida, no porque añada un tiempo infinito sino porque quita las ansias de inmortalidad.
      ==========

      """
    When we convert the input file to the org file "clippings.org"
    Then we should get an org file whose content is
      """
      * Epicuro
      ** Obras completas
      *** Acostúmbrate a pensar que la muerte no tiene nada que ver --
      Acostúmbrate a pensar que la muerte no tiene nada que ver con nosotros, porque todo bien y todo mal radica en la sensación, y la muerte es la privación de sensación. De ahí que la idea correcta de que la muerte no tiene nada que ver con nosotros hace gozosa la mortalidad de la vida, no porque añada un tiempo infinito sino porque quita las ansias de inmortalidad.
      /Highlight on Location 1186-1188. [2019-12-27 13:48:52]./

      """

  Scenario: several clippings from the same author and title should be ordered by location
    Given the kindle generated clipping file "My Clippings2.txt" whose content is
      """
      Obras completas (Epicuro)
      - Your Highlight on Location 1186-1188 | Added on Friday, December 27, 2019 1:48:52 PM

      Acostúmbrate a pensar que la muerte no tiene nada que ver con nosotros, porque todo bien y todo mal radica en la sensación, y la muerte es la privación de sensación. De ahí que la idea correcta de que la muerte no tiene nada que ver con nosotros hace gozosa la mortalidad de la vida, no porque añada un tiempo infinito sino porque quita las ansias de inmortalidad.
      ==========
      Obras completas (Epicuro)
      - Your Highlight on Location 1195-1197 | Added on Friday, December 27, 2019 1:53:33 PM

      Pero el sabio ni rehúsa vivir ni teme no vivir, pues ni le ofende el vivir ni se imagina que es un mal el no vivir. Y de la misma manera que de la comida no prefiere en absoluto la más abundante sino la más agradable, así también disfruta del tiempo no del más largo sino del más agradable.
      ==========

      """
    When we convert the input file to the org file "clippings2.org"
    Then we should get an org file whose content is
      """
      * Epicuro
      ** Obras completas
      *** Acostúmbrate a pensar que la muerte no tiene nada que ver --
      Acostúmbrate a pensar que la muerte no tiene nada que ver con nosotros, porque todo bien y todo mal radica en la sensación, y la muerte es la privación de sensación. De ahí que la idea correcta de que la muerte no tiene nada que ver con nosotros hace gozosa la mortalidad de la vida, no porque añada un tiempo infinito sino porque quita las ansias de inmortalidad.
      /Highlight on Location 1186-1188. [2019-12-27 13:48:52]./
      *** Pero el sabio ni rehúsa vivir ni teme no vivir, pues ni le --
      Pero el sabio ni rehúsa vivir ni teme no vivir, pues ni le ofende el vivir ni se imagina que es un mal el no vivir. Y de la misma manera que de la comida no prefiere en absoluto la más abundante sino la más agradable, así también disfruta del tiempo no del más largo sino del más agradable.
      /Highlight on Location 1195-1197. [2019-12-27 13:53:33]./

      """

  Scenario: clippings from different authors should be ordered by author
    Given the kindle generated clipping file "My Clippings3.txt" whose content is
      """
      How to Read a Book (A Touchstone book) (Van Doren, Charles;Mortimer J. Adler)
      - Your Highlight on Location 579-581 | Added on Tuesday, September 3, 2019 5:56:47 PM

      A college degree ought to represent general competence in reading such that a graduate could read any kind of material for general readers and be able to undertake independent research on almost any subject (for that is what syntopical reading, among other things, enables you to do).
      ==========
      Cosmos (Carl Sagan)
      - Your Highlight on Location 3617-3618 | Added on Monday, September 2, 2019 8:09:26 AM

      If you wish to make an apple pie from scratch, you must first invent the universe.
      ==========

      """
    When we convert the input file to the org file "clippings3.org"
    Then we should get an org file whose content is
      """
      * Carl Sagan
      ** Cosmos
      *** If you wish to make an apple pie from scratch, you must --
      If you wish to make an apple pie from scratch, you must first invent the universe.
      /Highlight on Location 3617-3618. [2019-09-02 08:09:26]./
      * Van Doren, Charles;Mortimer J. Adler
      ** How to Read a Book (A Touchstone book)
      *** A college degree ought to represent general competence in --
      A college degree ought to represent general competence in reading such that a graduate could read any kind of material for general readers and be able to undertake independent research on almost any subject (for that is what syntopical reading, among other things, enables you to do).
      /Highlight on Location 579-581. [2019-09-03 17:56:47]./

      """

  Scenario: clippings from different books of a single author should be ordered by book title
    Given the kindle generated clipping file "My Clippings4.txt" whose content is
      """
      Punished by Rewards (Alfie Kohn)
      - Your Highlight on Location 104-106 | Added on Monday, December 9, 2019 11:45:44 PM

      The core of pop behaviorism is \"Do this and you'll get that.\" The wisdom of this technique is very rarely held up for inspection; all that is open to question is what exactly people will receive and under what circumstances it will be promised and delivered.
      ==========
      No Contest (Alfie Kohn)
      - Your Highlight on Location 3811-3813 | Added on Monday, December 9, 2019 11:11:05 PM

      Despite the productivity and sense of fulfillment that come from working together, we often act as if cooperation is something for which we must sit passively and wait, like a beautiful sunset. In fact, there is scarcely an arena of human life which cannot be transformed into a cooperative enterprise.
      ==========

      """
    When we convert the input file to the org file "clippings4.org"
    Then we should get an org file whose content is
      """
      * Alfie Kohn
      ** No Contest
      *** Despite the productivity and sense of fulfillment that --
      Despite the productivity and sense of fulfillment that come from working together, we often act as if cooperation is something for which we must sit passively and wait, like a beautiful sunset. In fact, there is scarcely an arena of human life which cannot be transformed into a cooperative enterprise.
      /Highlight on Location 3811-3813. [2019-12-09 23:11:05]./
      ** Punished by Rewards
      *** The core of pop behaviorism is \"Do this and you'll get --
      The core of pop behaviorism is \"Do this and you'll get that.\" The wisdom of this technique is very rarely held up for inspection; all that is open to question is what exactly people will receive and under what circumstances it will be promised and delivered.
      /Highlight on Location 104-106. [2019-12-09 23:45:44]./

      """

  Scenario: clippings in Chinese should be converted correctly
    Given the kindle generated clipping file "My Clippings5.txt" whose content is
      """
      彩图全解道德经 (国学典藏) (（春秋）老子)
      - Your Highlight on Location 1355-1358 | Added on Monday, December 23, 2019 6:23:03 PM

      最高的善就像水一样，水善于滋润万物却不与其争短长。它总是停留在众人不愿去的低洼之地，这种品德，最接近于“道”。上善的人总是甘居卑下的环境，心胸善于保持沉静而深远博大，待人善于相助、真诚可亲，说话善于信守诺言，为政善于治理，办事善于发挥所长，行动善于把握时机。正因为有不争的美德，所以才不会出现过失，招来怨咎
      ==========

      """
    When we convert the input file to the org file "clippings5.org"
    Then we should get an org file whose content is
      """
      * （春秋）老子
      ** 彩图全解道德经 (国学典藏)
      *** 最高的善就像水一样，水善于滋润万物却不与其争短长。它总是停留在众人不愿去的低洼之地，这种品德，最接近于“道”。上善的 --
      最高的善就像水一样，水善于滋润万物却不与其争短长。它总是停留在众人不愿去的低洼之地，这种品德，最接近于“道”。上善的人总是甘居卑下的环境，心胸善于保持沉静而深远博大，待人善于相助、真诚可亲，说话善于信守诺言，为政善于治理，办事善于发挥所长，行动善于把握时机。正因为有不争的美德，所以才不会出现过失，招来怨咎
      /Highlight on Location 1355-1358. [2019-12-23 18:23:03]./

      """

  Scenario: if the book title contains the Byte order mark (U+FEFF), it should be removed
    Given the kindle generated clipping file "My Clippings6.txt" whose content is
      """
      ﻿Your Money or Your Life (Vicki Robin)
      - Your Highlight on Location 215-215 | Added on Tuesday, January 3, 2017 10:13:51 AM

      It corrodes society and the psyche—saps our belief in justice and fairness and hope.
      ==========
      黃金時代 (王小波)
      - Your Highlight on Location 365-365 | Added on Monday, February 13, 2017 5:09:34 PM

      沒必要做的事就別做
      ==========
      Your Money or Your Life (Vicki Robin)
      - Your Highlight on Location 2560-2561 | Added on Thursday, February 16, 2017 10:15:25 AM

      What do you now spend to simply compensate for doing a job that claims the majority of your waking hours?
      ==========

      """
    When we convert the input file to the org file "clippings6.org"
    Then we should get an org file whose content is
      """
      * Vicki Robin
      ** Your Money or Your Life
      *** It corrodes society and the psyche—saps our belief in --
      It corrodes society and the psyche—saps our belief in justice and fairness and hope.
      /Highlight on Location 215-215. [2017-01-03 10:13:51]./
      *** What do you now spend to simply compensate for doing a job --
      What do you now spend to simply compensate for doing a job that claims the majority of your waking hours?
      /Highlight on Location 2560-2561. [2017-02-16 10:15:25]./
      * 王小波
      ** 黃金時代
      *** 沒必要做的事就別做 --
      沒必要做的事就別做
      /Highlight on Location 365-365. [2017-02-13 17:09:34]./

      """
