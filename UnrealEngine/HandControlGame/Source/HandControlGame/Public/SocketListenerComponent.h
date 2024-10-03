// SocketListenerComponent.h

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "SocketListenerComponent.generated.h"

// Delegate for broadcasting actions received from the socket
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnActionEvent, const FString&, Action, const FString&, State);

/**
 * USocketListenerComponent
 * Component that listens for socket messages and dispatches action events.
 */
UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class HANDCONTROLGAME_API USocketListenerComponent : public UActorComponent, public FRunnable
{
    GENERATED_BODY()

public:
    // Sets default values for this component's properties
    USocketListenerComponent();

protected:
    // Called when the game starts
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

    // FRunnable interface
    virtual uint32 Run() override;
    virtual void Stop() override;

private:
    // Socket variables
    FSocket* ListenerSocket;
    FSocket* ConnectionSocket;
    FRunnableThread* ListenThread;
    bool bShouldRun;

    // Configuration
    UPROPERTY(EditAnywhere, Category = "Socket Listener")
    FString SocketDescription;

    UPROPERTY(EditAnywhere, Category = "Socket Listener")
    int32 Port;

    // Functions
    void InitializeSocket();
    void ShutdownSocket();
    void HandleReceivedData(FString& Buffer);

public:
    // Delegate for broadcasting action events
    UPROPERTY(BlueprintAssignable, Category = "Socket Listener")
    FOnActionEvent OnActionReceived;
};
