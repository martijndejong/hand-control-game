// MyPlayerController.cpp

#include "MyPlayerController.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"

AMyPlayerController::AMyPlayerController()
{
    // Create the SocketListenerComponent and attach it to the controller
    SocketListener = CreateDefaultSubobject<USocketListenerComponent>(TEXT("SocketListenerComponent"));

    // Initialize action states
    bIsMovingRight = false;
    bIsMovingLeft = false;
    bIsJumping = false;
}

void AMyPlayerController::BeginPlay()
{
    Super::BeginPlay();

    if (SocketListener)
    {
        // Bind to the OnActionReceived delegate
        SocketListener->OnActionReceived.AddDynamic(this, &AMyPlayerController::HandleActionEvent);
    }
}

void AMyPlayerController::SetupInputComponent()
{
    Super::SetupInputComponent();

    // Bind input functions for keyboard input (if needed)
    InputComponent->BindAxis("MoveRight", this, &AMyPlayerController::MoveRight);
    InputComponent->BindAction("Jump", IE_Pressed, this, &AMyPlayerController::Jump);
    InputComponent->BindAction("Jump", IE_Released, this, &AMyPlayerController::StopJumping);
}

void AMyPlayerController::HandleActionEvent(const FString& Action, const FString& State)
{
    UE_LOG(LogTemp, Log, TEXT("Action: %s, State: %s"), *Action, *State);

    // Handle the action and state combinations
    if (Action == "Move Right")
    {
        if (State == "start")
        {
            bIsMovingRight = true;
        }
        else if (State == "stop")
        {
            bIsMovingRight = false;
        }
    }
    else if (Action == "Move Left")
    {
        if (State == "start")
        {
            bIsMovingLeft = true;
        }
        else if (State == "stop")
        {
            bIsMovingLeft = false;
        }
    }
    else if (Action == "Jump")
    {
        if (State == "start")
        {
            bIsJumping = true;
            Jump();
        }
        else if (State == "stop")
        {
            bIsJumping = false;
            StopJumping();
        }
    }
    else if (Action == "Move Right and Jump")
    {
        if (State == "start")
        {
            bIsMovingRight = true;
            if (!bIsJumping)
            {
                bIsJumping = true;
                Jump();
            }
        }
        else if (State == "stop")
        {
            bIsMovingRight = false;
            if (bIsJumping)
            {
                bIsJumping = false;
                StopJumping();
            }
        }
    }
    else if (Action == "Move Left and Jump")
    {
        if (State == "start")
        {
            bIsMovingLeft = true;
            if (!bIsJumping)
            {
                bIsJumping = true;
                Jump();
            }
        }
        else if (State == "stop")
        {
            bIsMovingLeft = false;
            if (bIsJumping)
            {
                bIsJumping = false;
                StopJumping();
            }
        }
    }
}

void AMyPlayerController::MoveRight(float Value)
{
    // Combine keyboard input and gesture input
    float Direction = Value;

    if (bIsMovingRight)
    {
        Direction += 1.0f;
    }
    if (bIsMovingLeft)
    {
        Direction -= 1.0f;
    }

    // Clamp the direction to [-1, 1]
    Direction = FMath::Clamp(Direction, -1.0f, 1.0f);

    if (APawn* ControlledPawn = GetPawn())
    {
        ControlledPawn->AddMovementInput(FVector(0.0f, -1.0f, 0.0f), Direction);
    }
}

void AMyPlayerController::Jump()
{
    if (ACharacter* ControlledCharacter = Cast<ACharacter>(GetPawn()))
    {
        ControlledCharacter->Jump();
    }
}

void AMyPlayerController::StopJumping()
{
    if (ACharacter* ControlledCharacter = Cast<ACharacter>(GetPawn()))
    {
        ControlledCharacter->StopJumping();
    }
}
