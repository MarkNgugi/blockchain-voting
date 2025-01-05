from django.shortcuts import render, redirect
from web3 import Web3
import json
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

 
# Connect to Ganache
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load ABI and bytecode only when necessary
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from web3 import Web3
import json
from .models import Candidate, VotingTimeframe

# Connect to Ganache
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

def get_contract():
    abi_path = "voting_system/blockchain/build/Voting_sol_Voting.abi"
    contract_address = "0x7F0a4e2Cc173Dc51A49D69A1b930d449D7d6737f"
    checksum_address = Web3.to_checksum_address(contract_address)

    with open(abi_path) as abi_file:
        abi = json.load(abi_file)

    return web3.eth.contract(address=checksum_address, abi=abi)

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Candidate, VotingTimeframe

from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from .models import Candidate, VotingTimeframe

from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from .models import Candidate, VotingTimeframe



def student_register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            admission_number = form.cleaned_data['admission_number']
            
            # Check if the admission number is valid
            if not ValidAdmissionNumber.objects.filter(admission_number=admission_number).exists():
                messages.error(request, "Invalid admission number. Please ensure your admission number is valid.")
                return render(request, 'voting/register.html', {'form': form})
            
            # Check if the admission number already exists in the User model
            if User.objects.filter(username=admission_number).exists():
                messages.error(request, "This admission number is already registered.")
                return render(request, 'voting/register.html', {'form': form})
            
            password = form.cleaned_data['password']

            # Create a new User account for the student
            user = User.objects.create_user(username=admission_number, password=password)
            user.save()

            # Link the User to the Student model
            student = form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, "Registration successful!")
            return redirect('dashboard')  

    else:
        form = StudentRegistrationForm()

    return render(request, 'voting/register.html', {'form': form})


def student_login(request):
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            admission_number = form.cleaned_data['admission_number']
            password = form.cleaned_data['password']

            # Authenticate the student
            user = authenticate(username=admission_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard') 

            messages.error(request, "Invalid admission number or password.")
    
    else:
        form = StudentLoginForm()

    return render(request, 'voting/login.html', {'form': form})   
 
@login_required
def dashboard(request):
    current_time = timezone.now()
    timeframe = VotingTimeframe.objects.first()

    if not timeframe:
        return render(request, 'voting/not_available.html')

    start_time = timeframe.start_time
    end_time = timeframe.end_time
    start_time = timezone.localtime(start_time)
    end_time = timezone.localtime(end_time)
    current_time = timezone.localtime(current_time)

    if current_time < start_time:
        messages.info(request, f"Voting will start at {start_time}.")
        return render(request, "voting/not_available.html", {"message": f"Voting will start at {start_time}."})

    # Voting has ended, show the final results
    if current_time > end_time:
        # Fetch candidates from the blockchain
        contract = get_contract()
        candidates_count = contract.functions.candidatesCount().call()

        candidates_from_contract = [
            contract.functions.getCandidate(i).call()
            for i in range(candidates_count)
        ]

        # Filter out "Candidate 1" and "Candidate 2" from the list
        candidates_with_votes = [
            {"name": candidate[0], "id": i, "vote_count": candidate[1]}
            for i, candidate in enumerate(candidates_from_contract)
            if candidate[0] not in ["Candidate 1", "Candidate 2"]
        ]

        # Prepare context to display the candidates and their votes from blockchain
        context = {
            "candidates_from_blockchain": candidates_with_votes,
            "message": "Voting has ended. Results will be displayed below."
        }

        return render(request, "voting/not_available.html", context)

    # Voting is active, show candidates
    contract = get_contract()
    candidates_count = contract.functions.candidatesCount().call()

    candidates_from_contract = [
        contract.functions.getCandidate(i).call()
        for i in range(candidates_count)
    ]

    candidates_with_votes = [
        {"name": candidate[0], "id": i, "vote_count": candidate[1]}
        for i, candidate in enumerate(candidates_from_contract)
        if candidate[0] not in ["Candidate 1", "Candidate 2"]
    ]

    # Candidates from the Django model
    candidates_from_model = Candidate.objects.all()

    # Prepare context to display the candidates and their votes from blockchain
    context = {
        "candidates_from_blockchain": candidates_with_votes,
        "candidates_from_model": candidates_from_model,
    }

    return render(request, "voting/dashboard.html", context)





# Vote for a candidate
@login_required
def vote(request, candidate_id):
    contract = get_contract()
    user_address = web3.eth.accounts[1]  # Assuming student is using the second account

    print(f"DEBUG: Attempting to vote for candidate ID: {candidate_id}")

    try:
        # Fetch the candidate from Django DB
        candidate = Candidate.objects.get(id=candidate_id)

        # If blockchain_id is None, raise an error
        if candidate.blockchain_id is None:
            messages.error(request, "This candidate has not been added to the blockchain.")
            return redirect("dashboard")

        # Check the total number of candidates in the contract
        candidates_count = contract.functions.candidatesCount().call()
        print(f"DEBUG: Candidates Count on Blockchain: {candidates_count}")

        # Ensure the candidate_id is within the valid range
        if candidate.blockchain_id >= candidates_count:
            messages.error(request, "Invalid candidate. The candidate does not exist.")
            return redirect("dashboard")

        # Check if the user has already voted
        if contract.functions.hasVoted(user_address).call():
            messages.error(request, "You have already voted and cannot vote again.")
            return redirect("dashboard")

        # Cast the vote
        tx_hash = contract.functions.vote(candidate.blockchain_id).transact({"from": user_address})
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        # Update the vote count in the Django model after voting
        blockchain_vote_count = contract.functions.getCandidate(candidate.blockchain_id).call()[1]
        candidate.vote_count = blockchain_vote_count
        candidate.save()

        messages.success(request, "Your vote has been cast successfully!")

    except Candidate.DoesNotExist:
        messages.error(request, "Candidate does not exist.")
    except Exception as e:
        messages.error(request, f"An error occurred while voting: {str(e)}")
    
    return redirect("dashboard")



@staff_member_required
def admin_dashboard(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')
    
    contract = get_contract()

    candidates_count = contract.functions.candidatesCount().call()
    print("Number of candidates:", candidates_count)
    
    # Fetch candidates from the blockchain
    candidates_from_contract = [
        contract.functions.getCandidate(i).call()
        for i in range(candidates_count)
    ]
    
    # Filter out "Candidate 1" and "Candidate 2" from the list
    candidates_with_votes = [
        {"name": candidate[0], "id": i, "vote_count": candidate[1]}
        for i, candidate in enumerate(candidates_from_contract)
        if candidate[0] not in ["Candidate 1", "Candidate 2"]
    ]

    candidates_from_model = Candidate.objects.all()

    return render(request, "voting/admin_dashboard.html", {
        "candidates": candidates_with_votes,
        "candidates_from_model": candidates_from_model,
    })


# Add Candidate (Admin only)
def add_candidate(request):
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()

            contract = get_contract()
            user_address = web3.eth.accounts[0]  # Assuming the owner is using the first account

            try:
                # Add candidate to the blockchain
                tx_hash = contract.functions.addCandidate(candidate.name).transact({"from": user_address})
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                # Update the candidate object with the blockchain ID
                # The blockchain ID should be the total number of candidates after the new one is added
                candidate.blockchain_id = contract.functions.candidatesCount().call() - 1  # Blockchain ID is zero-based
                candidate.save()

                messages.success(request, "Candidate added successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred while adding candidate: {str(e)}")
            
            return redirect("admin_dashboard")
    else:
        form = CandidateForm()

    return render(request, "voting/add_candidate.html", {"form": form})



 

def set_voting_timeframe(request):
    timeframe = VotingTimeframe.objects.first()  # There should only be one timeframe
    if request.method == "POST":
        form = VotingTimeframeForm(request.POST, instance=timeframe)
        if form.is_valid():
            form.save()
            messages.success(request, "Voting timeframe updated successfully!")
            return redirect("admin_dashboard")
    else:
        form = VotingTimeframeForm(instance=timeframe)

    return render(request, "voting/set_voting_timeframe.html", {"form": form}) 