// MyPlayerController.h

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "SocketListenerComponent.h"
#include "MyPlayerController.generated.h"

/**
 * AMyPlayerController
 * Custom player controller that handles input from SocketListenerComponent
 */
UCLASS()
class HANDCONTROLGAME_API AMyPlayerController : public APlayerController
{
    GENERATED_BODY()

public:
    AMyPlayerController();

protected:
    virtual void BeginPlay() override;
    virtual void SetupInputComponent() override;

    // Handler function for action events
    UFUNCTION()
    void HandleActionEvent(const FString& Action, const FString& State);

    // Input functions
    void MoveRight(float Value);
    void Jump();
    void StopJumping();

private:
    // Reference to the SocketListenerComponent
    UPROPERTY()
    USocketListenerComponent* SocketListener;

    // Action states
    bool bIsMovingRight;
    bool bIsMovingLeft;
    bool bIsJumping;
};
