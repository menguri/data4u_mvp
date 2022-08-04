from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from accounts.forms import UserForm
from django.contrib import messages
import requests
from accounts.models import Profile
# Create your views here.


def kakaoPay(request):
    if request.method == 'POST' :
        _admin_key = 'e7b6071057ccc32ec53f3df582246d77' # 입력필요
        _url = f'https://kapi.kakao.com/v1/payment/ready'
        _headers = {
            'Authorization': f'KakaoAK {_admin_key}',
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        }
        _data = {
            'cid': 'TC0ONETIME',
            'partner_order_id': 1001 , #주문번호
    	    'partner_user_id': request.user.id,   # 유저 아이디
    	    'item_name':'포인트',                   # 구매 물품 이름
    	    'quantity':1,                        # 구매 물품 가격
    	    'total_amount':request.POST['point'],                 # 구매 물품 가격
    	    'vat_amount':0,                    # 구매 물품 비과세
    	    'tax_free_amount':0,
    	    # 내 애플리케이션 -> 앱설정 / 플랫폼 - WEB 사이트 도메인에 등록된 정보만 가능합니다
    	    # * 등록 : http://IP:8000 
    	    'approval_url':'https://data4u-mvp.herokuapp.com/accounts/paySuccess', 
            'fail_url':'https://data4u-mvp.herokuapp.com/accounts/payFail',
            'cancel_url':'https://data4u-mvp.herokuapp.com/accounts/payCancel'
        }
        res = requests.post(_url, data=_data, headers=_headers)
        _result = res.json()
        request.session['tid'] = _result['tid']
        next_url = _result['next_redirect_pc_url']  
        return redirect(next_url)
    
    try:
        profile = get_object_or_404(Profile, user=request.user)
    except:
        messages.error(request, '프로필을 먼저 등록해주세요.')
        return redirect('accounts:profile', request.user.id)
    return render(request, 'accounts/kakaoPay.html')


def paySuccess(request):
    _url = 'https://kapi.kakao.com/v1/payment/approve'
    _admin_key = 'e7b6071057ccc32ec53f3df582246d77' # 입력필요
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}'
    }
    _data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'],
        'partner_order_id':1001,
        'partner_user_id':request.user.id,
        'pg_token': request.GET['pg_token']
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    #amount = _res.json()['amount']['total']
    _result = _res.json()
    context = {
        'res' : _result,
    }
    if _result.get('msg'):
        messages.success(request, f'포인트 충전을 실패했습니다.')
        context = {
        'partner_order_id': _result['partner_order_id'],
        'item_name': _result['item_name'],
        'approved_at': _result['approved_at'],
        'total': _result['amount']['total'],
    	}
        return render(request, 'accounts/payFail.html', context)
    else:
        # point 충전
        profile = get_object_or_404(Profile, user=request.user)
        profile.point += _result['amount']['total']
        profile.save()
        messages.success(request, f'{_result["amount"]["total"]} 포인트가 충전되었습니다.')
        return render(request, 'accounts/paySuccess.html', context)

        
def payFail(request):
    return render(request, 'accounts/payFail.html')

def payCancel(request):
    return render(request, 'accounts/payCancel.html')