/**
 * 대신고 AI 수학 탐구 성과공유회
 * 구글 드라이브 파일 권한 일괄 설정 스크립트
 * 
 * 목적: 200개 보고서 파일을 "링크 있는 모든 사용자 - 뷰어" 로 설정
 *       (미리보기 허용, 다운로드/복사 방지)
 * 
 * 실행 방법:
 *   1. https://script.google.com 접속
 *   2. 새 프로젝트 생성
 *   3. 이 코드 붙여넣기
 *   4. setPermissions 함수 선택 후 [실행] 클릭
 *   5. 구글 계정 권한 승인
 */

var FILE_IDS = [
    "1TD3zWBcV07hrtKnHn9DvQMtCJ5pZDuFn",
    "1eRck8WnGLSkQmKtb0zNXK0I9cEyiqyT4JANAhv3uG0c",
    "1ZZK-byFHGWKjfTgDGHS_6X6-yQLETFN9",
    "1SbusJipXlgA_qHMNOXBE4KfR8t9SQ9IP",
    "1jwIp6eV0ONdJsN5gdyefqNymQmI7o1C9",
    "1jcnhKnD8BKE3XIN2DVPP7cF8ZiAbMMLf",
    "1gdzn_dM9Qt2UK8A27P-Vlw7LTLFMCEoeu25ZZe5dc6A",
    "1TKl314g_fdZRCymKxzlunnz5cob3LHje",
    "1tGi8jIoOJsSgQi08CVYJSmX3Ukcg_DHY",
    "1xb1dGkAfAWj4H0RZgaHkoRQabytV05id",
    "1RyeDMck3ZOqhFmRdwbWqR2bw7C3fGA4p",
    "19MqXKmggbiyDyW9jxhKr_f8IkJECbK-N",
    "1Ko9hXuluJknq1mOR9RTzvUyqeLyBM_o1",
    "1_mu75VVosXAoArvYya_-GwbUCFU4_EEi",
    "1lqpidHCzt9F1qjNuxz9cnvWQU7n81QoY",
    "16CzKhjPpuAPgyengV92rufWibQXypWMPq86aUCG54Ck",
    "1H6UGIr4nGta69bFSF0Th8fM-6h9pigR_",
    "1eoyN4JxFPgULBo7P_tbzOslv2ATvY2FDMzNO0MfLDIQ",
    "1pDKBRVOkwh1LdhSg7lD4qZCX45TErLYw",
    "1XotbBwUCNH6x3VHfX5jmac5EFhVAt-s_D2-S8-MiiqM",
    "10HkpTNai79Q-kXgLZSME0JwXUjCZa9F_",
    "18oQoCZdPeye-jrUCVz_2nMHxdcjTN1ww",
    "1Zex-nCiWM2KmjT2NfnY7hyVa2gS5SoTO",
    "1KAIOfIHIqPIxhrWNLJE351qRC4UJ9i03",
    "1L2mW22-yt9-w3z4c1UPdAQXWwvoT2hsT",
    "1I9rhaHi_krYE281C-SsrrLf_t_0fLWp0",
    "1-pk2JpNupEaI9Yf9LasI4qmeHG_mOe7H",
    "1ikdSFnCEHy88uuLvLwfWQ504MWOEQB2o",
    "13EOcZ-sG25Ds82EF_k8oa6cnrVoiX6Cq",
    "11PRtxC5jVr2I99nnCv80ri-9WUYhXRmv",
    "1DQWh4tUUtjyEFKhMFMLa_xD94-hAf3pq",
    "1OkOt08GqsyGUmrlqP39nSiz7MMVbV9WE",
    "1efdX33aoa4M4j8cABQHT0yzSLrWT0r2o",
    "14Klvki1UfW_9ncH1VBOjMFhzksQpV7cS",
    "1cjAymnJOPPV33j7tOXb1oSfKPVoxzr48",
    "1EgfGc9saB7pUGQKSlF-orR3tOj2cWPx-",
    "14knq-H2WDFO3XUz4OjL5wQGtH3r2msTu",
    "16jHgF8WBnnlQtMKpdDxzVW5FqByZnhh4",
    "1W-mWEPRPSWEvPFrQOfHm5l9V5RtBqhx1",
    "1sq2v3kvHx0Fr9vyqPxz82ahdjw-z1eqPZRQbqMTVzbk",
    "1no-BVnE0IPFc-UfxIlW7KBaTmpHG-uof",
    "1vylcVRHZASCJg1BKvY2zvftf4pu546Dx",
    "1Rj01JzfKSVCnpOnfAJ3hR2WVNyDpUMhu",
    "1BPisegoX8yuEq6W7RO19QnLh7LBodcP6",
    "1kzHySmQ1-IRvZcqgmY5SEGupXRrfpTb4s6NXNb2XyJc",
    "1sFstliXTm0v45mQfKnLTZxwJ_kqT5N0J",
    "17OWhVZQdll1nlJGnM0FuakoK8ziVqcXG",
    "1K0LHD7MU0JNRqGmVRE4Oe7fmf9nag4HB",
    "1pdyUDNH4JkuuhX8-NI2uT5USgfcF4w4S",
    "1wPRKHWsX4DujUbauwfHGi6KG0rCSUw6n",
    "1-_ps_LFC2Mh7KvepAOpOHlHCnGtU4FPc",
    "1mE6uxuguII9ZvvUABEHGhKCuDHph7MAA",
    "1iDCwON0vc7FrMH6Jpp1Mk7UrlzonOvjF",
    "1htsVZKamgQ65uajRMuaZO53t6WuiSg6d",
    "1WlRGOeuyJ2xiYQ_uA89clm4coqciGz0l",
    "1Tlm9aPNh1xuVB4_lJJw0mOMU8iID8W6k",
    "11oIUlRYzgnMrowGUn4Ba5whlF8PvVayf",
    "1R7AtDgwIsWvW7f6tPXJnOrGvNIa12PBy",
    "1kTVz3rwjYJ8iBuJ2msc5rVh5MHYoB_Sk",
    "11g-xsKFYdIEIyLkk7rgv4la3LsQU5gDh",
    "1BJl2SR_zajE-KCI-pr9dwxnRSMVaEvVM",
    "1_qKPPGKmUGkWasJqHs2HcRiRkigBDuAo",
    "1jYz3IE7IE8w7upfUqdDHfUW7y5F1YH-r",
    "1rX7YW2MXWW9OhQjqDJk3o7ARmDmcXrIZ",
    "1QWZIcNcphRr4T04BsAO0mwp-BAbK0qYF",
    "1U4T3FAdix8BWdWySkn29HzHQpDHqbw2W",
    "1Bl0TXNrpIA7agWm27JVKupZ7tFcSh1oI",
    "1e_v4nOiJM8gq-fXQzVcSviTpdZxJpewK",
    "12J0cyIpyAxFI-bhsMkDjkGc3gM-Edj6s",
    "1lgbUUzbqHhaJOfKYwWuIj7UylI2ltqq9",
    "1BD8qGqFOSCEaY-HxhCmxJvWHuK87EWIQtEwc6eiCdu4",
    "1fZ_LsoZs8_RGepf1zLYs9cAb8uyyudb_",
    "1mOp-z_eKH967hztOnQU44p3aO04lxrDB",
    "18V71EZuf4iRtErR2-6DgG2WxgT_PB4R_",
    "1OmzhH9kvsJSK_jfOx68qfLv5zkCUZ-yE",
    "12iswWLfu_X811rHDapoLEfZmz99X7bAe",
    "1CAzekVtC147HSp4kMlW4b-i8PUP4x0yj",
    "1m_C-iayMLoc2yBXqA2khs8Aml1IreTuZ",
    "1jeBr7ODqyRE3VYkV2Dk9RQMcsJ9m0HqC",
    "1Ob84AIwh8Ck_ltxawAE1YTB29CkG5_Nw",
    "1rKUUZ9QADFNjkpi4wctcH13LDCQAvNAu",
    "1BcoD8uCff3iE2h2INEEZrJg_H6lLYlbBZMabMI_M1hM",
    "1eiYSAU1s0Wnrxov1EzZyGIaqHyWILIMQ",
    "1KpP3YUQHxS1P09yO0VkBdg-bj4pGIyNl",
    "13VW9DGXwcyOzKK5puC8agkEq0Bd2K4K44A9n4p3C9ck",
    "1d689XpfBz1FX_VWKD93vjX2Smay_IfHFkFwa8RGJgWQ",
    "1oyzLCDmqOkOqL4FZSH6395tQE69-5RGEhFVgCnnZjW0",
    "16tuM-G96mQbFoVYWJrWYAgH6jVYQ7XKW",
    "1yKT4YAr-UYhU6PE4lCKl6AknYzX41NkF",
    "1PQhvsckrESEJ7HcJlrIDLLO-njDTWdhB",
    "1nHJbVYrK2v8d6OUElYb_hnGughfA8qHn",
    "1Y51x_ma7rrZ-O3bt63wPlTA82Gg9ksDu",
    "1EKVrWuB3QPfuby6OjAPWe_39wXurd2md",
    "1KC58QNAe-vd39Qggi_GilkRZLj3CuS37wsF7eGCuS_U",
    "198UdmXyYDG6gNYgsgVhTnI14x5HMgAkO",
    "1CIj1NDnkJUcj3cRYPVxweyb4FMoYrUo0",
    "1RqvgUZNzmjHWd35Fhy7Q8y9ZP5itH45h08ZzLB6y1JA",
    "12RVusqcduvYoTHZmJsVRH_CKnocXSL3o",
    "1v4I4xwCrPoy_ssLygfZS6GDXF4FMSosT",
    "1Q2yyweDywJeHPM872KoxfHzyZbWrvLO1",
    "1Ogh8HOzdtu2JnF7oxCyIrZlGJj8ly7aa",
    "1tRq4OO5JFzX2qCqcLqEr-IhmqDd9AD3E",
    "1v_Mn_iUAGrhAWjon0djdwGBerHa4th3H",
    "1NQXvAvS7wQVRry38PLtnBo8KzQfH-Lt0",
    "1NafTI7A2Q8D9Ak0GGYSBBbACuxqpN2Y7",
    "1iGf25ZPQGJ39c3P6Ww2UlKKalQAUAM2G",
    "1xtsOi3KgqtRWEqCFzC74tKnJaIA5lcSb",
    "1c9eYOKzW35zEpCY3v_FoEWYBZE4JT87T",
    "1SOl2xTAFOIXTspseD2WQjwWwnll6suNU",
    "1Q27p74NChKC-vfJFa93I1whNs9wkAdWo",
    "1jdBMbv7E-rwGSTOR9BObJ2j7rdIUyVSF",
    "16y_gqzVTuEvkUrUF2jQ7VFgdCHBZOWQU",
    "1sB8yA-x7OMOf8IWtaEPJALh_08-ws9KA",
    "1i_kCLk4df7G5gpsChx5vrXUBofe9EHcZ",
    "1SqcTPQD2qqUYfGgEEVkwBVKzDxk2WlwY",
    "1I1TJ5CgpvQw1drvKbYxmCIpZwNIXWGfh",
    "1VVI71dIG5nwao5aqZjB6HBnS8bknTJxo",
    "1Z3YtvNXbzUez-2lputEuHAzQSM9U-28r",
    "1XT1nutkdeLEYWWVQSzVfLaFUj2z_WGFC",
    "1D7jq7L2on5tm52FrWyNcey64V4cH4_US",
    "162N-sKU_DLuO4i6M0ESEVkIG0ah2w4GzLJKJ8Dw455s",
    "1lGmpD3PKdQZcU6kIJDsLEBSuo_q-toyp",
    "1PNqBHq8R_i849Xd1Szh_Ij2WEcDOc4h8",
    "1POXuKB759mrytnhGTV9hRlZmuDCAX_-_",
    "18T28YHlMuv0hvHZ8j5vRjFSzbuN1xSZL",
    "1QGpucJ8rsK5jeVPBWKX7fXioayRzz1Y6",
    "1Rx2o2sx-TfyJ81amDYay-J_H7dDiJ-4X",
    "17sMW241j4DYVHRwE-4yWUQWg_q-RrjiR",
    "1Hqu-zF2TRf4hza2DHdFF99zThKp0IrKQ",
    "1vyYEg_SETpW12uw3Jubm3UY-9CJC62ec",
    "1519jdo4s_XWiF-8TyW4QhtuHzj1zLd8L",
    "1Smw-2Qg4R9sI9nBDlv-A_Mq1DfOevdF_",
    "1Th97awtWLxLbtguA96gFIGJRSoBxu0DX",
    "18H4e666LXyb8SWx1ROx3kqLrbRU4Lt00",
    "1nlkDTe4bZTAYFQ81sBuu7D1-shvcjSCS",
    "1wkvfNzTRja2rZS7exRdlovujXRJf_8nL",
    "1NxvzlE5AK0g-qFNCj2teJtRpLxZpYUPQ",
    "1nv50K0VE6W75_4Qu3LRXG6SoYV6Ex1iP",
    "1hlxT2Tt62vXS6Nr2RyEvL0ksz_X1WJoO",
    "1YYfefR4EQR0RfDG-fQUiNCzAzLzlEegM",
    "10VhO9tuJUdZZajfaukAWCZ7dBe_ttAMQ",
    "1gxMg_y1aB5HqDtvJfG_ggvf867Sm4YiP",
    "1kUWs3hhTkpW6tOuGCI6nOL0WIaIF99tk",
    "1fD4OYb_U3XFL99jxUYhRA5GXFkRJweCA",
    "1iCfkAMYb6y-vouxKd2SHa2-0jMvoMc3K",
    "19jCPiUmUtAaAJ1475RCpPTsn4RzF2eQ3",
    "1Jum4QG50hk4Ugo9hISqW8HI7IvrdjKD9",
    "1J3CS7ozhzD8rBsYDM7N7aBBSLiIC4KQj",
    "1J5SGem1edc0AjlSZXQikW832f_v_3Hh_",
    "1XnFEo7mEE0VA-TxKJugS1GvJ258cTD2p",
    "1cPueAjgtCaq3ku29St_eHsC_Duce1b4a",
    "1Q91bZbiq3-tVDT937KZ4QeT0thdWk1BE",
    "1FMEqfk3kqssf-ufQ7PL256ME_LKplsIW",
    "1nDJLcwMwq9kN-X_EzTbuPyfTnpKYhjhl",
    "1RNHfoHSHWH4_iXOqWqxHbr24n8ha6yPY",
    "1emRg-xi-zVDNgiXzL8qVX5STQDWNJoQ1UDqHm-K2-58",
    "1hlzEPPHgYH1PY09xBpYHAZGV8Em-t5jN",
    "1n8FvEKPXtCrbDoOASmC2Dqf9RvNdsyqC",
    "1L3RqWH8To_QLlrmBIrPtB6PLEESGWTh4",
    "1e4l7KHLwxfu5LK_3MypFSrh9DF7QnDw0",
    "1F9XYbIzOFL98rfcThhE8KVdTUayC3ebS",
    "1MTfOEfF2xZIjoZP1HwKdl7WxBCNROjvU",
    "1iV-rACh2isTIvRYzhZxRk68ghjdwUo14",
    "1fqGu7jnWG6_jXB9xHel--WzooSLsSDrS",
    "1_fA-XbBQk1VmK2khZ1RjmYPuFE9KqHYUauB-v-pr3BU",
    "1U-L_OMOKa0g5Yng-I03w_LUjK05212Do",
    "1qLCocewAbKXHwf5e52nPtg6yWBecIUE1",
    "1Mm7VWlVpJnLYJWxufEdIjYVHTYrWHuTa",
    "1XUEMm2vtVTNUvK-sr9Px0fTWNOEjWwhY",
    "1_543xBf06XZx1TavNZcaNP5cac-6xtRU",
    "12YUvErwDmuoS_mka6ntA2P9mbaXjV2CP",
    "1_MCWcCoS8E6VPFXYUZSBrRU03NtWSWIK",
    "1RnEhXGbXMjZ95xrrSBebZ2xVx34dZP13",
    "1yrZV5zAb4L_stmf6qVeAp_bcbKhtHB5e",
    "10cyjiz5ENk0izFH-xhH2GB4Xf_uFtFtN",
    "1e8H_I838S362dvt02juf-A68YZHc2UXT",
    "1vLNdv_bZJXtKm6Vg8IMOFgETToycA2mH",
    "1FSNnNFG5B0_0N8JbsdQycl1PfxJA0dqI",
    "1XV4q_ZIzsoQD3Q3FMOuPRAEMIIUfWFW5",
    "1mw3t2_4HE4dTK0YSUbfHh_subtnbeedy",
    "17sQW6qMsmv_ygF2ujwVRAFHg5_WgFkA5",
    "1iSZlhkUay-FsuHspmxr4N97hfh15CtQa",
    "1EFSOPJ_InpWteECBWSJ5LUhmXkwx1jeN",
    "1MbVBXnsHogcizwResqbGOm2CKDx2c9hh",
    "1m2s8zgELL2m9wci9VH-izKLMImItt77P",
    "1fXpjAksDqB9S0i7DjIBqrkAfFMnY_G8T",
    "1mAeixUnAJicLCfyBYtVnL8rxJNWUUknC",
    "1-ZYmqn3bIXDr6sWJGZwOx3dK-zZUahRH",
    "1uNYaxDH9H2NxheewBJp0wrla0QIPK90i",
    "1krQrbhPtRbgdD5cPBeyuWARlCgQfvvNQ",
    "1Il7puM74eoI1mz_5FhamC0j6qwxLsTyU",
    "1s05ohHlus1uW4JpGhriCpLNhmSBnhcIg",
    "1pOaEdwh__0bgSFOfeYXbCpzhO-PwZ3Lz",
    "1Y5m3nJoWmEQtWZ7JnVtGf288qNjcgEvTVCdC-yaAN_g",
    "1XkgQuN5OUDf_lmrCm0XsKFTT18qCcKYt",
    "1gIJuQ0mLWagV-zNLveYcwni5X28RQiRKbOnKRUrhB24",
    "1kPmvhYqjG9b7bQ_MuqLhFZWZncmXeuqb",
    "1h-aTCWKnV6K7ND_hU5wN2qZvypbGEtQc",
    "1bmMkDEnpmLYZHmGAE7MA7LFOP6LpgF1R",
    "1GIwEp1XQd8e0jp5d-usFVhusPOWJswpw"
];

function setPermissions() {
  var success = 0;
  var failed = [];
  
  for (var i = 0; i < FILE_IDS.length; i++) {
    var fid = FILE_IDS[i];
    try {
      var file = DriveApp.getFileById(fid);
      
      // 링크 있는 모든 사용자 - 뷰어 권한
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
      
      // 뷰어/댓글 작성자의 다운로드·인쇄·복사 방지 (Google 파일 형식에 적용)
      file.setViewersCanCopyContent(false);
      
      success++;
      if (i % 20 === 0) {
        Logger.log(i + '/' + FILE_IDS.length + ' 처리 중...');
        Utilities.sleep(100); // API 속도 제한 방지
      }
    } catch(e) {
      Logger.log('오류 [' + fid + ']: ' + e.message);
      failed.push(fid);
    }
  }
  
  Logger.log('=== 완료 ===');
  Logger.log('성공: ' + success + '개');
  Logger.log('실패: ' + failed.length + '개');
  if (failed.length > 0) {
    Logger.log('실패 목록: ' + failed.join(', '));
  }
}
